import unittest
from unittest.mock import MagicMock
from service import StudyPlanService

class TestStudyPlanService(unittest.TestCase):
    
    def test_add_study_plan_success(self):
        # 1. Arrange (Chuẩn bị dữ liệu và giả lập Repository)
        mock_repo = MagicMock()
        mock_repo.find_by_subject.return_value = None  # Giả lập môn học chưa tồn tại
        service = StudyPlanService(mock_repo)
        
        # 2. Act (Thực thi hành động)
        result = service.add_study_plan("Lập trình Python", 15.0, "2026-06-01")
        
        # 3. Assert (Kiểm tra kết quả)
        self.assertTrue(result)
        mock_repo.save.assert_called_once()

    def test_add_study_plan_duplicate_subject(self):
        # 1. Arrange
        mock_repo = MagicMock()
        mock_repo.find_by_subject.return_value = "Exist"  # Giả lập đã tồn tại môn học
        service = StudyPlanService(mock_repo)
        
        # 2 & 3. Act & Assert (Kiểm tra ngoại lệ trùng tên)
        with self.assertRaises(ValueError) as context:
            service.add_study_plan("Lập trình Python", 15.0, "2026-06-01")
        
        self.assertEqual(str(context.exception), "Môn học 'Lập trình Python' đã tồn tại trong hệ thống!")

    def test_add_study_plan_invalid_hours(self):
        # 1. Arrange
        mock_repo = MagicMock()
        service = StudyPlanService(mock_repo)
        
        # 2 & 3. Act & Assert (Kiểm tra ngoại lệ giờ học <= 0)
        with self.assertRaises(ValueError) as context:
            service.add_study_plan("Cơ sở dữ liệu", -5.0, "2026-06-01")
            
        self.assertEqual(str(context.exception), "Số giờ mục tiêu phải lớn hơn 0!")

if __name__ == '__main__':
    unittest.main()