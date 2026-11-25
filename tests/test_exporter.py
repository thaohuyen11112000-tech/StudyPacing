import csv
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.report_exporter import (
    _find_vietnamese_font,
    calculate_total_hours,
    export_to_csv,
    export_to_pdf,
    report_exporter,
)


def test_calculate_total_hours_normal_and_invalid():
    records = [
        {"exercise": "Bài 1", "status": "Xong", "hours": 1.5},
        {"exercise": "Bài 2", "status": "Đang làm", "hours": "2.25"},
        {"exercise": "Bài 3", "status": "Hủy", "hours": -3},
        {"exercise": "Bài 4", "status": "Lỗi", "hours": "abc"},
    ]
    assert calculate_total_hours(records) == 3.75
    assert calculate_total_hours([]) == 0.0


def test_export_to_csv_creates_valid_file(tmp_path):
    csv_file = tmp_path / "out" / "bao_cao.csv"
    records = [
        {"exercise": "Ôn tập CSDL", "status": "Hoàn thành", "hours": 1.5},
        {"exercise": "Luyện Python", "status": "Đang học", "hours": 2},
    ]

    returned_path = export_to_csv(
        records=records,
        output_path=str(csv_file),
        learner_name="Trần Văn B",
    )

    assert returned_path == str(csv_file)
    assert csv_file.exists()

    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    assert ["Người học", "Trần Văn B"] in rows
    assert ["STT", "Bài tập", "Trạng thái", "Số giờ học"] in rows
    assert ["1", "Ôn tập CSDL", "Hoàn thành", "1.5"] in rows
    assert ["", "", "Tổng số giờ đã học", "3.5"] in rows


def test_find_vietnamese_font_missing_raises(monkeypatch):
    monkeypatch.setattr(os.path, "isfile", lambda _path: False)
    with pytest.raises(FileNotFoundError):
        _find_vietnamese_font(custom_font_path="khong_ton_tai_font_nao.ttf")

def test_export_to_pdf_with_real_system_font(tmp_path):
    font_candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    available_font = next((p for p in font_candidates if os.path.isfile(p)), None)
    if not available_font:
        pytest.skip("Không tìm thấy font hệ thống phù hợp để test PDF")

    pdf_file = tmp_path / "bao_cao.pdf"
    records = [{"exercise": "Học thuật toán", "status": "Xong", "hours": 2.5}]

    out = export_to_pdf(
        records=records,
        output_path=str(pdf_file),
        learner_name="Minh",
        font_path=available_font,
    )

    assert out == str(pdf_file)
    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 0


def test_report_exporter_dispatcher_and_invalid_format(tmp_path):
    records = [{"exercise": "Bài tập 1", "status": "Xong", "hours": 1.0}]
    csv_out = tmp_path / "dispatch.csv"

    res = report_exporter(
        records=records,
        export_format=" CSV ",
        output_path=str(csv_out),
    )
    assert res == str(csv_out)
    assert csv_out.exists()

    with pytest.raises(ValueError):
        report_exporter(records=records, export_format="xlsx")