import unittest
import os
from storage_system import save_json, load_json

class TestStorageSystem(unittest.TestCase):
    
    def setUp(self):
        """Tạo file dữ liệu tạm trước khi test"""
        self.test_file = "test_data.json"

    def tearDown(self):
        """Dọn dẹp xóa file tạm sau khi test xong"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_json(self):
        """Unit test 1: Kiểm tra lưu và đọc file JSON thành công"""
        data = [{"id": 1, "task": "Học Git"}]
        
        # Test hàm lưu
        is_saved = save_json(self.test_file, data)
        self.assertTrue(is_saved)
        
        # Test hàm đọc
        loaded_data = load_json(self.test_file, [])
        self.assertEqual(loaded_data, data)

    def test_load_non_existent_file(self):
        """Unit test 2: Kiểm tra đọc file không tồn tại sẽ trả về giá trị mặc định"""
        default_val = []
        result = load_json("non_existent_file.json", default_val)
        self.assertEqual(result, default_val)

if __name__ == "__main__":
    unittest.main()
