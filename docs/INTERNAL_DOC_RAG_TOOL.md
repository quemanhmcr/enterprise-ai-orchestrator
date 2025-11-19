# Internal Document RAG Tool

## 📖 Tổng Quan

RAG (Retrieval-Augmented Generation) Tool cho phép agents truy vấn tài liệu nội bộ của công ty bằng semantic search và LLM.

### Tính Năng Chính

- ✅ Semantic search trên PDF, TXT, DOCX, MD files
- ✅ Persistent vector storage với ChromaDB
- ✅ **Sử dụng Ollama - LLM local miễn phí 100%!**
- ✅ Free HuggingFace embeddings (chạy local)
- ✅ Tự động indexing và caching
- ✅ Hỗ trợ multiple agents chia sẻ cùng knowledge base
- ✅ **Không cần API key, hoạt động offline!**

## 🚀 Cài Đặt

### 1. Cài Ollama (LLM Local)

**Windows:**
```powershell
# Download và cài: https://ollama.com/download/windows
# Sau khi cài, pull model nhỏ:
ollama pull qwen2.5:0.5b
```

**Xem hướng dẫn chi tiết:** [`docs/OLLAMA_SETUP.md`](./OLLAMA_SETUP.md)

### 2. Cài Dependencies

```bash
# Cài đặt tất cả dependencies
uv pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface
```

### 3. Cấu Hình Environment (Optional)

File `.env` (có thể bỏ qua - dùng defaults):

```env
# Ollama config (optional - defaults shown)
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Thêm Tài Liệu

Đặt tài liệu nội bộ vào `shared/documents/`:

```
shared/documents/
├── sample_company_policy.md    # Sample đã có sẵn
├── your_policy.pdf             # Thêm PDF của bạn
├── technical_docs.md           # Thêm docs kỹ thuật
└── storage/                    # Auto-generated vector DB
```

## 💡 Cách Sử Dụng

### Sử Dụng Cơ Bản (Standalone)

```python
from shared.tools.internal_doc_rag_tool import create_internal_doc_rag_tool

# Tạo tool
rag_tool = create_internal_doc_rag_tool()

# Query documents
result = rag_tool._run(query="How many vacation days do employees get?")
print(result)
```

### Sử Dụng Với CrewAI Agent

```python
from crewai import Agent, Task, Crew, LLM
from shared.tools.internal_doc_rag_tool import create_internal_doc_rag_tool

# Tạo RAG tool
rag_tool = create_internal_doc_rag_tool()

# Tạo LLM config
llm = LLM(
    model="glm-4.6",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.3
)

# Tạo agent với RAG tool
hr_agent = Agent(
    role="HR Assistant",
    goal="Answer employee questions about company policies",
    backstory="Experienced HR professional",
    tools=[rag_tool],  # ← Thêm RAG tool vào đây
    llm=llm,
    verbose=True
)

# Tạo task
task = Task(
    description="What is our vacation policy?",
    expected_output="Clear explanation of vacation policy",
    agent=hr_agent
)

# Run crew
crew = Crew(agents=[hr_agent], tasks=[task])
result = crew.kickoff()
```

### Multiple Agents Sharing RAG

```python
# Tạo 1 RAG tool instance duy nhất
rag_tool = create_internal_doc_rag_tool()

# Nhiều agents dùng chung
hr_agent = Agent(role="HR", tools=[rag_tool], ...)
finance_agent = Agent(role="Finance", tools=[rag_tool], ...)
legal_agent = Agent(role="Legal", tools=[rag_tool], ...)

crew = Crew(agents=[hr_agent, finance_agent, legal_agent], ...)
```

## 🧪 Test & Examples

### Chạy Examples

```bash
# Chạy example script
python examples/rag_tool_usage.py
```

Example script bao gồm:
1. ✅ Basic standalone usage
2. ✅ Single agent with RAG
3. ✅ Multiple agents collaboration
4. ✅ Adding custom documents dynamically

### Test Queries

Thử các câu hỏi sau với sample document:

```python
queries = [
    "How many vacation days do employees get after 5 years?",
    "What is the work from home policy?",
    "What are the health insurance benefits?",
    "How much is the 401k matching?",
    "What is the professional development budget?",
]

for query in queries:
    result = rag_tool._run(query=query)
    print(f"Q: {query}\nA: {result}\n")
```

## 📊 Advanced Usage

### Custom Storage Locations

```python
rag_tool = InternalDocRAGTool(
    documents_dir="./custom/docs/path",
    persist_dir="./custom/storage/path",
    collection_name="my_custom_collection"
)
```

### Add Documents Programmatically

```python
# Add new documents to existing index
rag_tool.add_documents([
    "path/to/new_policy.pdf",
    "path/to/new_doc.md"
])
```

### Refresh Index

```python
# Rebuild index from scratch (sau khi thêm/xóa nhiều docs)
rag_tool.refresh_index()
```

## 🔧 Cấu Trúc Code

```
shared/
├── tools/
│   ├── __init__.py                      # Export InternalDocRAGTool
│   └── internal_doc_rag_tool.py         # Main RAG implementation
└── documents/
    ├── README.md                         # Documentation
    ├── sample_company_policy.md          # Sample document
    └── storage/                          # ChromaDB vector database
        └── chroma.sqlite3                # Auto-generated
```

## 🎯 Use Cases Trong Enterprise System

### 1. HR Crew
```python
# HR agents query policies, benefits, procedures
hr_tools = [rag_tool, SerperDevTool()]
hr_agent = Agent(role="HR Specialist", tools=hr_tools, ...)
```

### 2. Finance Crew
```python
# Finance agents query financial policies, budgets, compliance docs
finance_agent = Agent(role="CFO", tools=[rag_tool], ...)
```

### 3. Operations Crew
```python
# Operations query SOPs, workflows, quality standards
ops_agent = Agent(role="Operations Manager", tools=[rag_tool], ...)
```

### 4. Product Development Crew
```python
# Product team query technical specs, architecture docs
product_agent = Agent(role="Product Manager", tools=[rag_tool], ...)
```

### 5. Sales & Marketing Crew
```python
# Sales team query product info, pricing, sales playbooks
sales_agent = Agent(role="Sales Director", tools=[rag_tool], ...)
```

## ⚙️ Configuration

### LLM Settings

Tool sử dụng settings từ `Settings` object của LlamaIndex:

```python
# In internal_doc_rag_tool.py
Settings.llm = OpenAI(model="glm-4.6", ...)
Settings.embed_model = OpenAIEmbedding(...)
Settings.chunk_size = 512
Settings.chunk_overlap = 50
```

### Query Engine Parameters

```python
query_engine = index.as_query_engine(
    similarity_top_k=3,        # Top 3 relevant chunks
    response_mode="compact",   # Compact response
)
```

## 🐛 Troubleshooting

### Issue: "No documents found"

**Solution:** Thêm documents vào `shared/documents/` directory

```bash
# Check documents
ls shared/documents/

# Add sample doc if missing
cp sample_company_policy.md shared/documents/
```

### Issue: "Import Error: llama-index not found"

**Solution:** Install dependencies

```bash
uv sync
# hoặc
pip install llama-index llama-index-vector-stores-chroma
```

### Issue: "API Key Error"

**Solution:** Kiểm tra `.env` file

```bash
# Check environment
cat .env | grep OPENAI

# Reload environment
source .env  # Linux/Mac
# hoặc restart terminal on Windows
```

### Issue: Index không update sau khi thêm docs

**Solution:** Refresh index

```python
rag_tool.refresh_index()
```

## 📝 Best Practices

1. **Shared Tool Instance:** Tạo 1 instance duy nhất và share giữa agents
2. **Document Organization:** Organize docs theo category trong subdirectories
3. **Periodic Refresh:** Refresh index khi add/remove nhiều documents
4. **Version Control:** Thêm `storage/` vào `.gitignore`
5. **Security:** Không commit sensitive documents

## 🔐 Security Notes

⚠️ **Quan trọng:**

- Thêm `shared/documents/storage/` vào `.gitignore`
- Không commit sensitive internal documents
- Use environment variables cho API keys
- Consider encryption cho sensitive data

## 📚 Resources

- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [CrewAI Tools Guide](https://docs.crewai.com/core-concepts/tools/)

---

**Created:** November 18, 2025  
**Version:** 1.0.0  
**Maintained by:** Enterprise AI Team
