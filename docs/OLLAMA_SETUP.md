# RAG Tool với Ollama - Hướng dẫn Setup

## 🚀 Ollama - LLM Local Miễn Phí

Ollama cho phép chạy LLM models locally trên máy của bạn - **100% miễn phí, không cần API key!**

## 📥 Bước 1: Cài đặt Ollama

### Windows:
1. Download Ollama: https://ollama.com/download/windows
2. Chạy file installer `OllamaSetup.exe`
3. Ollama sẽ tự động chạy ở background

### Kiểm tra cài đặt:
```powershell
ollama --version
```

## 📦 Bước 2: Pull Model nhỏ gọn

Chọn 1 trong các models sau (từ nhỏ đến lớn):

```powershell
# Model siêu nhỏ - 0.5GB (Recommended cho RAM thấp)
ollama pull qwen2.5:0.5b

# Model nhỏ - 1.7GB (Recommended)
ollama pull phi3:mini

# Model vừa - 1.6GB
ollama pull gemma2:2b

# Model tốt hơn - 4.7GB
ollama pull qwen2.5:3b
```

### Kiểm tra models đã cài:
```powershell
ollama list
```

## ⚙️ Bước 3: Cấu hình Environment

Thêm vào file `.env`:

```env
# Ollama Configuration (Optional - có defaults)
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_BASE_URL=http://localhost:11434
```

**Lưu ý:** Nếu không set, tool sẽ dùng mặc định `qwen2.5:0.5b`

## 🔧 Bước 4: Cài Python Dependencies

```powershell
uv pip install llama-index-llms-ollama
```

## ✅ Bước 5: Test RAG Tool

```powershell
.\.venv\Scripts\python.exe test_rag_tool.py
```

## 📊 So sánh Models

| Model | Size | RAM cần | Tốc độ | Chất lượng |
|-------|------|---------|--------|------------|
| qwen2.5:0.5b | 0.5GB | 2GB | Rất nhanh | Đủ dùng |
| phi3:mini | 1.7GB | 4GB | Nhanh | Tốt |
| gemma2:2b | 1.6GB | 4GB | Nhanh | Tốt |
| qwen2.5:3b | 4.7GB | 8GB | Vừa | Rất tốt |

## 🎯 Recommended Setup

Cho hầu hết các trường hợp:
```powershell
ollama pull qwen2.5:0.5b
```

Trong `.env`:
```env
OLLAMA_MODEL=qwen2.5:0.5b
```

## 🔍 Test Ollama trực tiếp

```powershell
# Test chat với model
ollama run qwen2.5:0.5b

# Gõ câu hỏi và nhấn Enter
# Gõ /bye để thoát
```

## 🐛 Troubleshooting

### Lỗi: "Could not connect to Ollama"
**Giải pháp:** 
```powershell
# Khởi động lại Ollama service
ollama serve
```

### Lỗi: "Model not found"
**Giải pháp:**
```powershell
# Pull model lại
ollama pull qwen2.5:0.5b
```

### Ollama chạy chậm
**Giải pháp:**
- Dùng model nhỏ hơn (qwen2.5:0.5b)
- Đóng các ứng dụng khác
- Kiểm tra RAM còn trống

## 📝 Sử dụng RAG Tool

```python
from shared.tools.internal_doc_rag_tool import create_internal_doc_rag_tool

# Tool tự động dùng Ollama
rag_tool = create_internal_doc_rag_tool()

# Query documents
result = rag_tool._run(query="How many vacation days do employees get?")
print(result)
```

## 🌟 Ưu điểm Ollama

✅ **Miễn phí 100%** - Không cần API key  
✅ **Private** - Data không rời khỏi máy bạn  
✅ **Offline** - Hoạt động không cần internet  
✅ **Nhanh** - Chạy local, không có network latency  
✅ **Dễ dùng** - Setup trong 5 phút  

## 🔗 Links hữu ích

- Ollama Website: https://ollama.com
- Ollama Models Library: https://ollama.com/library
- Ollama GitHub: https://github.com/ollama/ollama
- LlamaIndex Ollama Docs: https://docs.llamaindex.ai/en/stable/examples/llm/ollama/

---

**Created:** November 18, 2025  
**Version:** 1.0.0
