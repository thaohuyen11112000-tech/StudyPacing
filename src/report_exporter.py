
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