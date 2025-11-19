"""
Internal Document RAG Tool
RAG tool for querying internal company documents using LlamaIndex
"""

import os
from pathlib import Path
from typing import Any, List, Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    import chromadb
    from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.gemini import Gemini
    from llama_index.vector_stores.chroma import ChromaVectorStore
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False


class InternalDocRAGInput(BaseModel):
    """Input schema for InternalDocRAGTool."""
    query: str = Field(..., description="Question or query to search in internal documents")


class InternalDocRAGTool(BaseTool):
    """
    RAG Tool for querying internal company documents.

    This tool uses LlamaIndex with ChromaDB to provide semantic search
    and question-answering capabilities over internal documentation.

    Features:
    - Semantic search over PDF, TXT, DOCX, MD files
    - Persistent vector storage with ChromaDB
    - Configurable embedding and LLM models
    - Support for glm-4.6 model via OpenAI-compatible API

    Usage:
        tool = InternalDocRAGTool(
            documents_dir="./shared/documents",
            persist_dir="./shared/documents/storage"
        )
        result = tool._run(query="What is our company's vacation policy?")
    """

    name: str = "Internal Document RAG"
    description: str = (
        "Search and query internal company documents. "
        "Use this tool to find information from internal policies, procedures, "
        "technical documentation, and other company knowledge base materials. "
        "Provide a clear question or search query."
    )
    args_schema: Type[BaseModel] = InternalDocRAGInput

    documents_dir: str = Field(
        default="./shared/documents",
        description="Directory containing internal documents"
    )
    persist_dir: str = Field(
        default="./shared/documents/storage",
        description="Directory for persistent vector storage"
    )
    collection_name: str = Field(
        default="internal_docs",
        description="ChromaDB collection name"
    )

    _index: Optional[Any] = None
    _initialized: bool = False

    def __init__(self, **data):
        """Initialize the RAG tool."""
        super().__init__(**data)

        if not LLAMA_INDEX_AVAILABLE:
            raise ImportError(
                "LlamaIndex is not installed. "
                "Install with: pip install llama-index llama-index-vector-stores-chroma"
            )

        # Convert to absolute paths
        self.documents_dir = str(Path(self.documents_dir).resolve())
        self.persist_dir = str(Path(self.persist_dir).resolve())

        # Create directories if they don't exist
        Path(self.documents_dir).mkdir(parents=True, exist_ok=True)
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)

    def _setup_llm_and_embedding(self):
        """Configure LLM and embedding models from environment."""
        # Get Gemini config from env or use defaults
        gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAZ8kMB__7VVHkCvqK3BW-yFtYLrRn-qLg")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")

        # Configure Gemini LLM (free API!)
        llm = Gemini(
            model=gemini_model,
            api_key=gemini_api_key,
            temperature=0.1,
        )

        # Configure FREE embedding model (HuggingFace - runs locally)
        # Using sentence-transformers model - no API key needed!
        embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5",  # Free, fast, multilingual
        )

        # Set global settings
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50

        return llm, embed_model

    def _initialize_index(self):
        """Initialize or load the vector index."""
        if self._initialized and self._index is not None:
            return self._index

        # Setup LLM and embedding
        self._setup_llm_and_embedding()

        # Initialize ChromaDB client
        chroma_client = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = chroma_client.get_or_create_collection(self.collection_name)

        # Create vector store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Check if documents directory has files
        documents_path = Path(self.documents_dir)
        has_documents = any(
            documents_path.glob(f"*.{ext}")
            for ext in ["pdf", "txt", "md", "docx", "doc"]
        )

        if has_documents:
            # Load documents
            try:
                documents = SimpleDirectoryReader(
                    self.documents_dir,
                    recursive=True,
                    required_exts=[".pdf", ".txt", ".md", ".docx", ".doc"]
                ).load_data()

                if documents:
                    # Create index from documents
                    self._index = VectorStoreIndex.from_documents(
                        documents,
                        storage_context=storage_context,
                        show_progress=True,
                    )
                    print(f"✓ Indexed {len(documents)} documents from {self.documents_dir}")
                else:
                    # Create empty index
                    self._index = VectorStoreIndex.from_documents(
                        [],
                        storage_context=storage_context,
                    )
                    print(f"⚠ No documents found in {self.documents_dir}")
            except Exception as e:
                print(f"⚠ Error loading documents: {e}")
                # Create empty index
                self._index = VectorStoreIndex.from_documents(
                    [],
                    storage_context=storage_context,
                )
        else:
            # Create empty index
            self._index = VectorStoreIndex.from_documents(
                [],
                storage_context=storage_context,
            )
            print(f"⚠ No documents found in {self.documents_dir}")

        self._initialized = True
        return self._index

    def _run(self, query: str) -> str:
        """
        Execute the RAG query.

        Args:
            query: The search query or question

        Returns:
            Answer based on the internal documents
        """
        try:
            # Initialize index if not already done
            index = self._initialize_index()

            # Create query engine
            query_engine = index.as_query_engine(
                similarity_top_k=3,
                response_mode="compact",
            )

            # Execute query
            response = query_engine.query(query)

            # Format response
            result = f"Answer: {response.response}\n\n"

            # Add source information if available
            if hasattr(response, 'source_nodes') and response.source_nodes:
                result += "Sources:\n"
                for i, node in enumerate(response.source_nodes, 1):
                    # Get filename from metadata
                    filename = node.metadata.get('file_name', 'Unknown')
                    score = node.score if hasattr(node, 'score') else 'N/A'
                    result += f"{i}. {filename} (relevance: {score:.2f})\n"

            return result

        except Exception as e:
            return (
                f"Error querying internal documents: {str(e)}\n\n"
                f"Please ensure documents are available in {self.documents_dir}"
            )

    def add_documents(self, file_paths: List[str]) -> str:
        """
        Add new documents to the index.

        Args:
            file_paths: List of file paths to add

        Returns:
            Status message
        """
        try:
            # Initialize index
            index = self._initialize_index()

            # Load new documents
            new_docs = []
            for file_path in file_paths:
                if Path(file_path).exists():
                    docs = SimpleDirectoryReader(
                        input_files=[file_path]
                    ).load_data()
                    new_docs.extend(docs)

            if new_docs:
                # Insert documents into index
                for doc in new_docs:
                    index.insert(doc)

                return f"Successfully added {len(new_docs)} documents to the index"
            else:
                return "No valid documents found to add"

        except Exception as e:
            return f"Error adding documents: {str(e)}"

    def refresh_index(self) -> str:
        """
        Rebuild the entire index from scratch.

        Returns:
            Status message
        """
        try:
            # Reset initialization flag
            self._initialized = False
            self._index = None

            # Reinitialize
            self._initialize_index()

            return "Index refreshed successfully"

        except Exception as e:
            return f"Error refreshing index: {str(e)}"


# Factory function for easy instantiation
def create_internal_doc_rag_tool(
    documents_dir: str = "./shared/documents",
    persist_dir: str = "./shared/documents/storage",
    collection_name: str = "internal_docs"
) -> InternalDocRAGTool:
    """
    Factory function to create an InternalDocRAGTool instance.

    Args:
        documents_dir: Directory containing internal documents
        persist_dir: Directory for persistent vector storage
        collection_name: ChromaDB collection name

    Returns:
        Configured InternalDocRAGTool instance
    """
    return InternalDocRAGTool(
        documents_dir=documents_dir,
        persist_dir=persist_dir,
        collection_name=collection_name
    )
