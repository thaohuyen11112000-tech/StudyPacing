from database import StudyPlanRepository
from service import StudyPlanService

def main():
    repo = StudyPlanRepository()
    service = StudyPlanService(repo)

    while True:
        print("\n========================================")
        print("    QUẢN LÝ TIẾN ĐỘ HỌC TẬP (STUDYPACING)")
        print("========================================")
        print("1. Thêm lộ trình học tập mới")
        print("2. Thoát chương trình")
        choice = input("Mời bạn chọn chức năng (1-2): ")

        if choice == "1":
            subject = input("Nhập tên môn học: ")
            try:
                hours = float(input("Nhập số giờ mục tiêu: "))
                deadline = input("Nhập hạn chót (YYYY-MM-DD): ")
                service.add_study_plan(subject, hours, deadline)
                print(" Thêm lộ trình học tập thành công!")
            except ValueError as e:
                print(f" Lỗi: {e}")
        elif choice == "2":
            print("Tạm biệt hệ thống StudyPacing!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại từ 1 đến 2.")

if __name__ == "__main__":
    main()