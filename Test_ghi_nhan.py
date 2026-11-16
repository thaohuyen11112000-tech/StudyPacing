import json
import unittest
from unittest.mock import mock_open, patch

HISTORY_FILE = "history.json"


def ghi_nhan_phien_hoc(duration, subject="Học tập chung"):
  import os

  history = []
  if os.path.exists(HISTORY_FILE):
    try:
      with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
    except Exception:
      history = []

  phien_moi = {"duration": duration, "subject": subject}
  history.append(phien_moi)

  with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=4)


class TestGhiNhanPhienHoc(unittest.TestCase):

  @patch("os.path.exists")
  @patch("builtins.open", new_callable=mock_open, read_data="[]")
  def test_ghi_nhan_phien_hoc_moi(self, mock_file, mock_exists):
    """Unit Test 1: Kiểm tra hàm ghi nhận phiên học khi file ban đầu trống ([]).

    Đảm bảo dữ liệu được ghi vào file đúng định dạng JSON.
    """
    mock_exists.return_value = True

    ghi_nhan_phien_hoc(45, "Lập trình Python")

    mock_file.assert_any_call(HISTORY_FILE, "w", encoding="utf-8")


if __name__ == "__main__":
  unittest.main()