import unittest
from study_goal import StudyGoal

class TestStudyGoal(unittest.TestCase):
    
    # Test 1: Kiểm thử khi nhập số phút hợp lệ (> 0)
    def test_set_target_valid(self):
        goal = StudyGoal()
        result = goal.set_target(90)
        self.assertTrue(result)
        self.assertEqual(goal.target_minutes, 90)

    # Test 2: Kiểm thử khi nhập số phút không hợp lệ (<= 0) phải bắn ra lỗi ValueError
    def test_set_target_invalid(self):
        goal = StudyGoal()
        with self.assertRaises(ValueError):
            goal.set_target(0)

if __name__ == '__main__':
    unittest.main()