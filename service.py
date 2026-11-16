from database import StudyPlan

class StudyPlanService:
    def __init__(self, repository):
        self.repository = repository

    def add_study_plan(self, subject_name, target_hours, deadline):
        """Kiểm tra logic nghiệp vụ trước khi lưu vào CSDL"""
        if not subject_name or subject_name.strip() == "":
            raise ValueError("Tên môn học không được để trống!")
        
        if target_hours <= 0:
            raise ValueError("Số giờ mục tiêu phải lớn hơn 0!")

        # Kiểm tra trùng lặp tên môn học
        existing = self.repository.find_by_subject(subject_name)
        if existing:
            raise ValueError(f"Môn học '{subject_name}' đã tồn tại trong hệ thống!")

        # Tạo object và lưu
        new_plan = StudyPlan(id=None, subject_name=subject_name, target_hours=target_hours, deadline=deadline)
        self.repository.save(new_plan)
        return True