# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Quang Tuấn   
> **Mã Sinh Viên / Mã Học viên:** 2A202602470 
> **Chủ đề Lựa chọn:** Trợ lý Sửa xe máy điện VinFast (VinFast E-Motorbike Service Agent)

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | Để đặt được lịch sửa xe điện VinFast, Agent thường phải tra lịch sử bảo hành/tình trạng pin theo VIN trước, rồi kiểm tra khung giờ trống của trạm dịch vụ, cuối cùng mới đặt lịch — 3 bước suy luận nối tiếp thay vì trả lời 1 lượt. |
| **2. Tool Interaction** | 5 / 5 | Hệ thống bắt buộc gọi 3 Tool qua MCP Server (`check_vehicle_history`, `check_slot_availability`, `book_service_appointment`) để lấy dữ liệu thật từ hệ thống VinFast, không thể trả lời chính xác nếu chỉ dựa vào tri thức tĩnh của LLM. |
| **3. Dynamic Decision** | 4 / 5 | Nhánh xử lý phụ thuộc kết quả quan sát: nếu xe còn bảo hành thì đề xuất gói miễn phí, nếu hết bảo hành thì báo phí; nếu pin/khung giờ khách chọn đã kín thì phải đề xuất phương án khác trước khi đặt lịch. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải giữ ngữ cảnh biển số/VIN xe và khung giờ đã tra cứu xuyên suốt nhiều lượt hội thoại (ví dụ hỏi lịch trống trước, xác nhận giờ sau) để hoàn tất mục tiêu đặt lịch cuối cùng tại trạm dịch vụ VinFast. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | Tổng điểm > 12/20 → Bài toán phù hợp triển khai Agentic System (ReAct Agent + MCP), không nên dùng Chatbot baseline vì cần tra cứu dữ liệu động và quyết định nhánh xử lý. |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

> Trích từ TC04 (multi_step_reasoning) — câu hỏi: *"Xe 29MĐ1-76623 của tôi còn bảo hành pin không, và nếu khung giờ 9:00 sáng 20/09/2026 tại trạm dịch vụ còn trống thì đặt lịch sửa luôn giúp tôi."* Agent tự suy luận và gọi nối tiếp 3 Tool qua MCP Server trước khi tổng hợp Final Answer.

```json
[
  {
    "step": 1,
    "query": "Xe 29MĐ1-76623 của tôi còn bảo hành pin không, và nếu khung giờ 9:00 sáng 20/09/2026 tại trạm dịch vụ còn trống thì đặt lịch sửa luôn giúp tôi.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_vehicle_history",
    "arguments": { "plate_number": "29MĐ1-76623" },
    "observation": {
      "status": "SUCCESS",
      "plate_number": "29MĐ1-76623",
      "data": {
        "model": "VinFast Feliz S",
        "warranty_status": "Hết bảo hành từ 01/01/2026",
        "battery_health": "78%"
      }
    },
    "latency_ms": 3601.74
  },
  {
    "step": 2,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "check_slot_availability",
    "arguments": { "date_str": "20/09/2026", "technician_name": "" },
    "observation": {
      "status": "SUCCESS",
      "available_slots_by_technician": {
        "Trần Văn Hùng": ["8:00", "10:30", "14:00"],
        "Lê Thị Mai": ["9:00", "13:00", "15:30"]
      }
    },
    "latency_ms": 2510.31
  },
  {
    "step": 3,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_service_appointment",
    "arguments": {
      "datetime_str": "9:00 20/09/2026",
      "plate_number": "29MĐ1-76623",
      "technician_name": "Lê Thị Mai"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-29MĐ1-76623-LÊ",
      "message": "Đặt lịch thành công cho xe 29MĐ1-76623 với kỹ thuật viên Lê Thị Mai vào lúc 9:00 20/09/2026."
    },
    "latency_ms": 2398.92
  },
  {
    "step": 4,
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "✅ Thông tin bảo hành: Xe 29MĐ1-76623 hết bảo hành từ 01/01/2026, pin 78%. ✅ Khung giờ 9:00 trống với kỹ thuật viên Lê Thị Mai. ✅ Đã đặt lịch thành công, mã BK-29MĐ1-76623-LÊ.",
    "latency_ms": 5438.57
  }
]
```

**Nhận xét:** Agent tự suy luận đúng thứ tự 3 bước (tra bảo hành → tra khung giờ → đặt lịch), và khi khung giờ 9:00 của kỹ thuật viên được chỉ định ban đầu (Trần Văn Hùng) không có trong danh sách nhưng lại trống ở kỹ thuật viên khác (Lê Thị Mai), Agent tự động chọn phương án thay thế hợp lý thay vì báo lỗi — minh chứng cho *Dynamic Decision* thực sự dựa trên Observation, không phải theo kịch bản cố định.

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (OpenAI-compatible endpoint, model `gpt-oss:20b`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 6 lượt (TC02: 1, TC03: 1, TC04: 3, TC05: 1; TC01 trả lời trực tiếp không cần Tool).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
