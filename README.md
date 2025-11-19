# Hệ Thống AI Doanh Nghiệp (Enterprise Business AI System)
**Điều Phối Đa Đội Ngũ với CEO AI**

## 🏗️ Tổng Quan Kiến Trúc

Đây là hệ thống AI cấp doanh nghiệp (Enterprise-grade), sẵn sàng cho môi trường production, được thiết kế theo tiêu chuẩn Big Tech:
- **6 Đội Ngũ (Crews):** 1 CEO Điều Phối + 5 Đội Ngũ Chuyên Môn (Kinh doanh, Sản phẩm, Vận hành, Tài chính, Marketing).
- **Tính Năng Nâng Cao:** Tích hợp Memory (Bộ nhớ), Knowledge (Tri thức), Flows (Luồng xử lý), Guardrails (Kiểm soát an toàn).
- **Sẵn Sàng Production:** Hỗ trợ Docker containerization, CI/CD pipeline, và cấu trúc dự án tiêu chuẩn.
- **Kiến Trúc Tập Trung:** CEO Crew đóng vai trò trung tâm, điều phối các đội ngũ chuyên môn thông qua cơ chế Tool-use.

## 📁 Cấu Trúc Dự Án

```
enterprise_business_system/
├── crews/                          # Triển khai các đội ngũ AI
│   ├── ceo_crew/                  # CEO Orchestrator (Điều phối)
│   ├── market_research_crew/      # Nghiên cứu thị trường
│   ├── product_development_crew/  # Phát triển sản phẩm
│   ├── sales_marketing_crew/      # Kinh doanh & Tiếp thị
│   ├── operations_crew/           # Vận hành
│   └── finance_crew/              # Tài chính
├── shared/                        # Tài nguyên chia sẻ (Memory, Tools, Utils)
├── .github/                       # CI/CD Workflows
├── tests/                         # Unit & Integration Tests
├── Dockerfile                     # Cấu hình Docker
├── Makefile                       # Các lệnh tiện ích
└── main.py                        # Điểm khởi chạy chính
```

## 🎯 Tổng Quan Các Đội Ngũ AI

1.  **👔 CEO Crew (Điều Phối):** Ra quyết định chiến lược, lập kế hoạch và điều phối hoạt động giữa các phòng ban. **Đặc biệt:** CEO Crew sử dụng các Crew khác như những công cụ (tools) để thực thi nhiệm vụ, tạo nên mô hình quản lý tập trung.
2.  **📊 Market Research Crew:** Thu thập dữ liệu thị trường, phân tích đối thủ cạnh tranh và dự báo xu hướng.
3.  **🚀 Product Development Crew:** Đổi mới sáng tạo, quản lý vòng đời sản phẩm và đảm bảo chất lượng (QA).
4.  **💰 Sales & Marketing Crew:** Thúc đẩy doanh thu, xây dựng thương hiệu và quản lý quan hệ khách hàng (CRM).
5.  **⚙️ Operations Crew:** Tối ưu hóa quy trình vận hành, quản lý chuỗi cung ứng và đánh giá rủi ro.
6.  **💵 Finance Crew:** Lập kế hoạch tài chính, kiểm soát ngân sách và đảm bảo tuân thủ quy định.

## 🔧 Tính Năng Kỹ Thuật Nổi Bật

-   **Hệ Thống Bộ Nhớ Đa Tầng:** Kết hợp Short-term (ngữ cảnh hiện tại), Long-term (lịch sử), và Entity Memory (nhận diện thực thể).
-   **Quản Lý Tri Thức (RAG):** Tích hợp tài liệu nội bộ, dữ liệu thị trường thời gian thực.
-   **Cơ Chế Guardrails:** Đảm bảo an toàn dữ liệu, kiểm tra định dạng và tuân thủ chính sách AI.
-   **Khả Năng Mở Rộng:** Thiết kế để scale ngang (Horizontal Scaling) trên Kubernetes.

## 🚀 Bắt Đầu Nhanh (Quick Start)

### Yêu Cầu Tiên Quyết
-   Python 3.10+
-   `uv` (Modern Python package manager)

### Cài Đặt Môi Trường

```bash
# 1. Cài đặt uv
pip install uv

# 2. Cài đặt dependencies
uv sync

# 3. Thiết lập biến môi trường
cp .env.example .env
# -> Cập nhật API keys (OpenAI, Anthropic...) trong file .env
```

### Vận Hành Hệ Thống

**Môi Trường Phát Triển (Development):**
```bash
# 1. Chạy luồng điều phối chính (CEO Flow)
# Cách 1: Chạy tương tác (Interactive Mode)
python main.py --orchestrate

# Cách 2: Chạy với yêu cầu cụ thể (Direct Input)
python main.py --orchestrate --input "Xây dựng chiến lược mở rộng thị trường sang Đông Nam Á với ngân sách 2 triệu đô"

# 2. Chạy riêng lẻ một đội ngũ (Ví dụ: Market Research)
# Chạy với input tùy chỉnh
python main.py --crew market_research --input "Phân tích thị trường xe điện tại Việt Nam"
```

**Môi Trường Production:**
```bash
# Build Docker Image
make docker-build

# Run Docker Container
make docker-run
```

## 🧪 Kiểm Thử (Testing)

```bash
# Chạy toàn bộ test suite
pytest tests/

# Kiểm tra độ bao phủ (Coverage)
pytest --cov=crews --cov=flows tests/
```

## 🛠️ Tech Stack

-   **Core Framework:** CrewAI (Multi-agent Orchestration)
-   **LLM Interface:** LiteLLM
-   **Vector Database:** ChromaDB
-   **Infrastructure:** Docker, GitHub Actions (CI/CD)
-   **Monitoring:** Prometheus, Grafana

---
**Dự án mẫu Enterprise AI - Tài liệu nội bộ cho Thực tập sinh & Developer**
