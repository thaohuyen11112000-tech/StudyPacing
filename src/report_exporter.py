import csv
import os
from typing import Any, Dict, List
from fpdf import FPDF


def calculate_total_hours(sessions: List[Dict[str, Any]], tasks: List[Dict[str, Any]]) -> float:
    """Tính tổng số giờ đã học từ danh sách phiên học hoặc danh sách bài tập."""
    total_minutes = 0.0

    if sessions:
        for session in sessions:
            total_minutes += float(session.get("duration_minutes", 0) or 0)
    elif tasks:
        for task in tasks:
            total_minutes += float(task.get("completed_minutes", task.get("duration_minutes", 0)) or 0)

    return round(total_minutes / 60.0, 2)


def export_to_csv(
    file_path: str,
    tasks: List[Dict[str, Any]],
    sessions: List[Dict[str, Any]] | None = None,
) -> str:
    """Xuất lịch sử học và danh sách bài tập ra file CSV (không lỗi font tiếng Việt)."""
    sessions = sessions or []
    total_hours = calculate_total_hours(sessions, tasks)

    parent_dir = os.path.dirname(os.path.abspath(file_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    # Dùng utf-8-sig để Excel mở tiếng Việt có dấu chuẩn xác
    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["BÁO CÁO LỊCH SỬ HỌC TẬP - STUDYPACING"])
        writer.writerow(["Tổng số giờ đã học", f"{total_hours} giờ"])
        writer.writerow([])
        writer.writerow(["STT", "Tiêu đề bài tập", "Trạng thái"])

        for idx, task in enumerate(tasks, start=1):
            title = task.get("title", "Không có tiêu đề")
            status = task.get("status", "Chưa hoàn thành")
            writer.writerow([idx, title, status])

    return file_path


def export_to_pdf(
    file_path: str,
    tasks: List[Dict[str, Any]],
    sessions: List[Dict[str, Any]] | None = None,
    font_path: str | None = None,
) -> str:
    """Xuất lịch sử học và danh sách bài tập ra file PDF (không lỗi font tiếng Việt)."""
    sessions = sessions or []
    total_hours = calculate_total_hours(sessions, tasks)

    parent_dir = os.path.dirname(os.path.abspath(file_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Nạp font tiếng Việt (.ttf) trên Windows
    font_name = "Helvetica"
    chosen_font = font_path or r"C:\Windows\Fonts\arial.ttf"
    if os.path.exists(chosen_font):
        pdf.add_font("VietFont", "", chosen_font, uni=True)
        font_name = "VietFont"

    pdf.set_font(font_name, size=14)
    pdf.cell(0, 10, text="BÁO CÁO LỊCH SỬ HỌC TẬP - STUDYPACING", ln=True)

    pdf.set_font(font_name, size=11)
    pdf.cell(0, 8, text=f"Tổng số giờ đã học: {total_hours} giờ", ln=True)
    pdf.ln(4)

    pdf.set_font(font_name, size=12)
    pdf.cell(0, 8, text="Danh sách bài tập:", ln=True)
    pdf.set_font(font_name, size=11)

    if not tasks:
        pdf.cell(0, 8, text="- Chưa có bài tập nào.", ln=True)
    else:
        for idx, task in enumerate(tasks, start=1):
            title = task.get("title", "Không có tiêu đề")
            status = task.get("status", "Chưa hoàn thành")
            pdf.multi_cell(0, 8, text=f"{idx}. {title} - Trạng thái: {status}")

    pdf.output(file_path)
    return file_paths