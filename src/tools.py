"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Trợ lý Sửa xe máy điện VinFast (VinFast E-Motorbike Service Agent)
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu lịch sử bảo dưỡng & tình trạng bảo hành / pin theo biển số xe
    {
        "name": "check_vehicle_history",
        "description": "Tra cứu lịch sử bảo dưỡng, tình trạng bảo hành và tình trạng pin của xe máy điện VinFast bằng biển số xe.",
        "parameters": {
            "type": "object",
            "properties": {
                "plate_number": {
                    "type": "string",
                    "description": "Biển số xe máy điện VinFast cần tra cứu (ví dụ: '29MĐ1-12345')"
                }
            },
            "required": ["plate_number"]
        }
    },

    # Tool 2: Tra cứu khung giờ trống tại trạm dịch vụ VinFast
    {
        "name": "check_slot_availability",
        "description": "Kiểm tra khung giờ trống của kỹ thuật viên tại trạm dịch vụ VinFast theo ngày và tên kỹ thuật viên (tùy chọn).",
        "parameters": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "Ngày cần kiểm tra lịch trống (ví dụ: '20/09/2026')"
                },
                "technician_name": {
                    "type": "string",
                    "description": "Tên kỹ thuật viên muốn kiểm tra lịch (ví dụ: 'Trần Văn Hùng'). Bỏ trống nếu muốn xem tất cả kỹ thuật viên."
                }
            },
            "required": ["date_str"]
        }
    },

    # Tool 3: Đặt lịch mang xe vào trạm dịch vụ VinFast
    {
        "name": "book_service_appointment",
        "description": "Đặt lịch hẹn mang xe máy điện VinFast vào trạm dịch vụ để bảo dưỡng/sửa chữa.",
        "parameters": {
            "type": "object",
            "properties": {
                "plate_number": {
                    "type": "string",
                    "description": "Biển số xe máy điện VinFast cần đặt lịch (ví dụ: '29MĐ1-12345')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '9:00 20/09/2026')"
                },
                "technician_name": {
                    "type": "string",
                    "description": "Tên kỹ thuật viên phụ trách ca sửa xe"
                }
            },
            "required": ["plate_number", "datetime_str", "technician_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_VEHICLE_DATABASE = {
    "29MĐ1-12345": {
        "model": "VinFast Evo200",
        "vin": "VF-EVO200-000123",
        "warranty_status": "Còn bảo hành đến 15/03/2027",
        "battery_health": "92%",
        "last_service_date": "10/06/2026",
        "last_service_note": "Bảo dưỡng định kỳ, kiểm tra phanh và pin"
    },
    "29MĐ1-76623": {
        "model": "VinFast Feliz S",
        "vin": "VF-FELIZS-000988",
        "warranty_status": "Hết bảo hành từ 01/01/2026",
        "battery_health": "78%",
        "last_service_date": "02/02/2026",
        "last_service_note": "Thay lốp trước, kiểm tra hệ thống điện"
    }
}

MOCK_SLOT_DATABASE = {
    "20/09/2026": {
        "Trần Văn Hùng": ["8:00", "10:30", "14:00"],
        "Lê Thị Mai": ["9:00", "13:00", "15:30"]
    }
}


def execute_check_vehicle_history(plate_number: str) -> str:
    """Thực thi tra cứu lịch sử bảo dưỡng & bảo hành theo biển số xe"""
    vehicle = MOCK_VEHICLE_DATABASE.get(plate_number.strip().upper())
    if vehicle:
        return json.dumps({
            "status": "SUCCESS",
            "plate_number": plate_number,
            "data": vehicle
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu xe máy điện VinFast có biển số '{plate_number}'"
        }, ensure_ascii=False)


def execute_check_slot_availability(date_str: str, technician_name: str = None) -> str:
    """Thực thi kiểm tra khung giờ trống tại trạm dịch vụ VinFast"""
    day_slots = MOCK_SLOT_DATABASE.get(date_str.strip())
    if not day_slots:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không có dữ liệu lịch trống cho ngày '{date_str}'"
        }, ensure_ascii=False)

    if technician_name:
        available = day_slots.get(technician_name.strip())
        if available is None:
            return json.dumps({
                "status": "NOT_FOUND",
                "message": f"Không tìm thấy kỹ thuật viên '{technician_name}' vào ngày '{date_str}'"
            }, ensure_ascii=False)
        return json.dumps({
            "status": "SUCCESS",
            "date": date_str,
            "technician_name": technician_name,
            "available_slots": available
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "date": date_str,
        "available_slots_by_technician": day_slots
    }, ensure_ascii=False)


def execute_book_service_appointment(plate_number: str, datetime_str: str, technician_name: str) -> str:
    """Thực thi đặt lịch hẹn sửa xe tại trạm dịch vụ VinFast"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{plate_number}-{technician_name[:3].upper()}",
        "plate_number": plate_number,
        "datetime": datetime_str,
        "technician_name": technician_name,
        "message": f"Đặt lịch thành công cho xe {plate_number} với kỹ thuật viên {technician_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "check_vehicle_history": execute_check_vehicle_history,
    "check_slot_availability": execute_check_slot_availability,
    "book_service_appointment": execute_book_service_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
