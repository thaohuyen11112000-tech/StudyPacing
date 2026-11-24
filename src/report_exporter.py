
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