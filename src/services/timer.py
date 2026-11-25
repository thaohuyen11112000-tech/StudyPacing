"""Đồng hồ đếm ngược chính xác theo thời gian thực (AC1).

Dùng mốc thời gian tuyệt đối (time.monotonic) thay vì đếm cộng dồn từng
giây, nên không bị lệch khi vòng lặp bị chậm hoặc máy bị treo ngắn.
Tham số `clock` cho phép giả lập thời gian khi kiểm thử.
"""
import time
from typing import Callable, Optional


class CountdownTimer:
    def __init__(self, seconds: float, clock: Callable[[], float] = time.monotonic):
        if seconds <= 0:
            raise ValueError("seconds phải > 0")
        self.total = float(seconds)
        self._clock = clock
        self._remaining = self.total
        self._end: Optional[float] = None

    @property
    def running(self) -> bool:
        return self._end is not None

    def start(self) -> None:
        if self.running:
            return
        self._end = self._clock() + self._remaining

    def pause(self) -> None:
        if not self.running:
            return
        self._remaining = max(0.0, self._end - self._clock())
        self._end = None

    def reset(self, seconds: Optional[float] = None) -> None:
        if seconds is not None:
            if seconds <= 0:
                raise ValueError("seconds phải > 0")
            self.total = float(seconds)
        self._remaining = self.total
        self._end = None

    def remaining(self) -> float:
        if self.running:
            return max(0.0, self._end - self._clock())
        return self._remaining

    def finished(self) -> bool:
        return self.remaining() <= 0.0


def format_mmss(seconds: float) -> str:
    """Làm tròn lên để không hiển thị 00:00 khi còn vài phần giây."""
    s = int(-(-seconds // 1))
    return f"{s // 60:02d}:{s % 60:02d}"
