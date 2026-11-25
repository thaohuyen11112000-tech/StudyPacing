
import csv
import os
from typing import Any, Dict, List, Optional
from fpdf import FPDF


def calculate_total_hours(records: List[Dict[str, Any]]) -> float:
    """Tính tổng số giờ đã học từ danh sách bài tập."""
    total = 0.0
    for item in records:
        try:
            hours = float(item.get("hours", 0) or 0)
            if hours > 0:
                total += hours
        except (ValueError, TypeError):
            continue
    return round(total, 2)
def export_to_csv(
    records: List[Dict[str, Any]],
    output_path: str = "lich_su_hoc.csv",
    learner_name: Optional[str] = None,
) -> str:
    """Xuất danh sách bài tập, trạng thái và tổng số giờ ra file .csv không lỗi tiếng Việt."""
    parent_dir = os.path.dirname(os.path.abspath(output_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    total_hours = calculate_total_hours(records)

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if learner_name:
            writer.writerow(["Người học", learner_name])
            writer.writerow([])
        writer.writerow(["STT", "Bài tập", "Trạng thái", "Số giờ học"])

        for idx, item in enumerate(records, start=1):
            exercise = str(item.get("exercise", ""))
            status = str(item.get("status", ""))
            try:
                hours = round(float(item.get("hours", 0) or 0), 2)
            except (ValueError, TypeError):
                hours = 0.0
            writer.writerow([idx, exercise, status, hours])

        writer.writerow([])
        writer.writerow(["", "", "Tổng số giờ đã học", total_hours])

    return output_path
def _find_vietnamese_font(custom_font_path: Optional[str] = None) -> str:
    """Tìm file font .ttf hỗ trợ tiếng Việt trên máy."""
    candidates: List[Optional[str]] = [
        custom_font_path,
        "DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in candidates:
        if path and os.path.isfile(path) and path.lower().endswith(".ttf"):
            return path

    raise FileNotFoundError(
        "Không tìm thấy font .ttf hỗ trợ tiếng Việt. Vui lòng truyền font_path hợp lệ."
    )
def export_to_pdf(
    records: List[Dict[str, Any]],
    output_path: str = "lich_su_hoc.pdf",
    learner_name: Optional[str] = None,
    font_path: Optional[str] = None,
) -> str:
    """Xuất danh sách bài tập, trạng thái và tổng số giờ ra file .pdf không lỗi tiếng Việt."""
    parent_dir = os.path.dirname(os.path.abspath(output_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    resolved_font = _find_vietnamese_font(font_path)
    total_hours = calculate_total_hours(records)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font("VNFont", style="", fname=resolved_font)
    pdf.set_font("VNFont", size=15)
    pdf.cell(0, 10, text="BÁO CÁO LỊCH SỬ HỌC TẬP", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(2)

    if learner_name:
        pdf.set_font("VNFont", size=11)
        pdf.cell(0, 8, text=f"Người học: {learner_name}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    col_widths = [15, 95, 45, 35]
    headers = ["STT", "Bài tập", "Trạng thái", "Số giờ học"]

    pdf.set_font("VNFont", size=10)
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 9, text=h, border=1, align="C")
    pdf.ln()

    for idx, item in enumerate(records, start=1):
        exercise = str(item.get("exercise", ""))
        status = str(item.get("status", ""))
        try:
            hours = round(float(item.get("hours", 0) or 0), 2)
        except (ValueError, TypeError):
            hours = 0.0

        pdf.cell(col_widths[0], 8, text=str(idx), border=1, align="C")
        pdf.cell(col_widths[1], 8, text=exercise, border=1, align="L")
        pdf.cell(col_widths[2], 8, text=status, border=1, align="C")
        pdf.cell(col_widths[3], 8, text=f"{hours:.2f}", border=1, align="R")
        pdf.ln()

    pdf.cell(
        col_widths[0] + col_widths[1] + col_widths[2],
        9,
        text="Tổng số giờ đã học",
        border=1,
        align="R",
    )
    pdf.cell(col_widths[3], 9, text=f"{total_hours:.2f} giờ", border=1, align="R")
    pdf.ln()

    pdf.output(output_path)
    return output_path
def report_exporter(
    records: List[Dict[str, Any]],
    export_format: str = "csv",
    output_path: Optional[str] = None,
    learner_name: Optional[str] = None,
    font_path: Optional[str] = None,
) -> str:
    """Hàm điều phối chính của US05: xuất lịch sử học ra file 'csv' hoặc 'pdf'."""
    fmt = export_format.strip().lower()
    if fmt == "csv":
        return export_to_csv(
            records=records,
            output_path=output_path or "bao_cao_lich_su_hoc.csv",
            learner_name=learner_name,
        )
    if fmt == "pdf":
        return export_to_pdf(
            records=records,
            output_path=output_path or "bao_cao_lich_su_hoc.pdf",
            learner_name=learner_name,
            font_path=font_path,
        )
    raise ValueError("Định dạng không hỗ trợ. Chỉ chấp nhận 'csv' hoặc 'pdf'.")
