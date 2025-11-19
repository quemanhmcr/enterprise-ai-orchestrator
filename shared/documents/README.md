# Internal Documents Directory

This directory contains internal company documents that will be indexed by the RAG system.

## Supported File Types
- PDF (`.pdf`)
- Text files (`.txt`)
- Markdown (`.md`)
- Word documents (`.docx`, `.doc`)

## Usage

1. Place your internal documents in this directory
2. The RAG tool will automatically index them on first use
3. To refresh the index after adding new documents, call `tool.refresh_index()`

## Vector Storage

The `storage/` subdirectory contains the ChromaDB vector database:
- Persistent storage for document embeddings
- Automatically created on first run
- Can be deleted to rebuild the index from scratch

## Example Documents Structure

```
documents/
├── policies/
│   ├── employee_handbook.pdf
│   ├── vacation_policy.md
│   └── code_of_conduct.pdf
├── technical/
│   ├── api_documentation.md
│   ├── system_architecture.pdf
│   └── deployment_guide.docx
├── financial/
│   ├── budget_guidelines.pdf
│   └── expense_policy.txt
└── storage/                    # Auto-generated vector DB
    └── chroma.sqlite3
```

## Security Note

⚠️ **Do not commit sensitive documents to version control!**

Add sensitive files to `.gitignore`:
```
shared/documents/*.pdf
shared/documents/**/*.docx
shared/documents/storage/
```
