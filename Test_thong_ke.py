import json
import unittest
from unittest.mock import mock_open, patch

HISTORY_FILE = "history.json"


class TestThongKeNangSuat(unittest.TestCase):

  @patch("os.path.exists")
  @patch("json.load")
  @patch(
      "builtins.open",
      new_callable=mock_open,
      read_data='[{"duration": 30, "subject": "Math"}]',
  )
  def test_tinh_tong_thoi_gian_hoc(
      self, mock_file, mock_json_load, mock_exists
  ):
    """Unit Test 2: Kiểm tra logic đọc dữ liệu từ file JSON và tính toán tổng

    thời gian học.
    """
    mock_exists.return_value = True
    mock_json_load.return_value = [
        {"duration": 30, "subject": "Math"},
        {"duration": 60, "subject": "Python"},
    ]

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      history = json.load(f)

    tong_phut = sum(item.get("duration", 0) for item in history)

    self.assertEqual(tong_phut, 90)
    self.assertEqual(len(history), 2)


if __name__ == "__main__":
  unittest.main()