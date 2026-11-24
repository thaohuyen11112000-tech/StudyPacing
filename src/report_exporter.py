import csv
from datetime import datetime
from fpdf import FPDF  # Cài bằng: pip install fpdf


def export_to_csv(tasks, total_hours, output_path="bao_cao_hoc_tap.csv"):
    """
    Xuất báo cáo ra file .csv hỗ trợ tiếng Việt (UTF-8 BOM cho Excel).
    tasks: list các dict, ví dụ: [{"title": "Ôn OOP", "status": "Hoàn thành"}]
    total_hours: float hoặc int (tổng số giờ đã học)
    """
    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["BÁO CÁO LỊCH SỬ HỌC TẬP - STUDYPACING"])
        writer.writerow(["Ngày xuất", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow(["Tổng số giờ đã học", f"{total_hours:.2f} giờ"])
        writer.writerow([])  # Dòng trống
        writer.writerow(["STT", "Bài tập", "Trạng thái"])

        for idx, task in enumerate(tasks, start=1):
            title = task.get("title", "")
            status = task.get("status", "")
            writer.writerow([idx, title, status])

    return output_path


def export_to_pdf(tasks, total_hours, font_path, output_path="bao_cao_hoc_tap.pdf"):
    """
    Xuất báo cáo ra file .pdf có tiếng Việt.
    font_path: đường dẫn tới file font .ttf hỗ trợ tiếng Việt (ví dụ: DejaVuSans.ttf hoặc Arial.ttf)
    """
    pdf = FPDF()
    pdf.add_page()

    # Đăng ký font tiếng Việt Unicode (thiết yếu để không lỗi dấu)
    pdf.add_font("VNFont", "", font_path, uni=True)
    pdf.set_font("VNFont", size=14)
    pdf.cell(0, 10, txt="BÁO CÁO LỊCH SỬ HỌC TẬP - STUDYPACING", ln=True, align="C")

    pdf.set_font("VNFont", size=11)
    pdf.cell(0, 8, txt=f"Ngày xuất: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, txt=f"Tổng số giờ đã học: {total_hours:.2f} giờ", ln=True)
    pdf.ln(5)

    pdf.set_font("VNFont", size=12)
    pdf.cell(0, 8, txt="Danh sách bài tập:", ln=True)

    pdf.set_font("VNFont", size=10)
    if not tasks:
        pdf.cell(0, 7, txt="- Chưa có dữ liệu bài tập.", ln=True)
    else:
        for idx, task in enumerate(tasks, start=1):
            title = task.get("title", "")
            status = task.get("status", "")
            pdf.cell(0, 7, txt=f"{idx}. {title} | Trạng thái: {status}", ln=True)

    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    sample_tasks = [
        {"title": "Làm bài tập Git & GitHub", "status": "Hoàn thành"},
        {"title": "Ôn tập thuật toán sắp xếp", "status": "Đang làm"},
        {"title": "Đọc tài liệu Python nâng cao", "status": "Chưa làm"},
    ]
    sample_hours = 6.5

    csv_file = export_to_csv(sample_tasks, sample_hours)
    print("Đã tạo CSV:", csv_file)

    # Thay đổi font_path sang file .ttf tiếng Việt có trên máy bạn (ví dụ C:/Windows/Fonts/arial.ttf)
    # pdf_file = export_to_pdf(sample_tasks, sample_hours, font_path="DejaVuSans.ttf")
    # print("Đã tạo PDF:", pdf_file)
