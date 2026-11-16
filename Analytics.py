import os
import json

HISTORY_FILE = "history.json"

def ghi_nhan_phien_hoc(duration, subject="Học tập chung"):
    """Hàm ghi lại phiên học vào file history.json."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    phien_moi = {
        "duration": duration,
        "subject": subject
    }
    history.append(phien_moi)
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
    print(f"✅ Đã ghi nhận: {duration} phút cho môn '{subject}'.")

def thong_ket_tong_quan():
    """Hàm thống kê năng suất học tập đầy đủ và chi tiết."""
    if not os.path.exists(HISTORY_FILE):
        print("\n❌ Chưa có dữ liệu học tập (history.json).")
        return
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []
        
    if not history:
        print("\n❌ Chưa có phiên học nào được ghi nhận.")
        return

    tong_so_phien = len(history)
    tong_phut = sum(item.get("duration", 0) for item in history)
    trung_binh_phut = round(tong_phut / tong_so_phien, 1) if tong_so_phien > 0 else 0
    
    print("\n========== BÁO CÁO THỐNG KÊ NĂNG SUẤT ==========")
    print(f"🎯 Tổng số phiên       : {tong_so_phien} phiên")
    print(f"⏳ Tổng thời gian      : {tong_phut} phút (~ {round(tong_phut/60, 1)} giờ)")
    print(f"📊 Trung bình mỗi phiên: {trung_binh_phut} phút")
    print("==================================================")

if __name__ == "__main__":
    # Khi chạy file chính, chỉ thực hiện nhiệm vụ chính là gọi hàm thống kê
    thong_ket_tong_quan()