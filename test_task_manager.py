import unittest
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def test_add_task_success(self):
        # 1. Arrange (Chuẩn bị dữ liệu)
        manager = TaskManager()
        task_title = "Học môn Công nghệ phần mềm"
        priority_level = "Cao"

        # 2. Act (Thực thi hàm thêm task)
        manager.add_task(task_title, priority_level)
        tasks = manager.get_all_tasks()

        # 3. Assert (Kiểm tra kết quả mong đợi)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], task_title)
        self.assertEqual(tasks[0]["priority"], priority_level)
        self.assertFalse(tasks[0]["completed"])

    def test_complete_task_success(self):
        # 1. Arrange (Chuẩn bị task sẵn có)
        manager = TaskManager()
        manager.add_task("Ôn tập Git", "Trung bình")

        # 2. Act (Thực thi đánh dấu hoàn thành task ở vị trí index = 0)
        manager.complete_task(0)
        tasks = manager.get_all_tasks()

        # 3. Assert (Kiểm tra trạng thái đã chuyển thành True / Done)
        self.assertTrue(tasks[0]["completed"])
        self.assertEqual(tasks[0]["status"], "Done")

if __name__ == "__main__":
    unittest.main()