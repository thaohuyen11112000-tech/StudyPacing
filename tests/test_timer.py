import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.timer import CountdownTimer, format_mmss


class FakeClock:
    def __init__(self, now: float = 100.0):
        self.now = now

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.mark.parametrize("bad_seconds", [0, -1, -0.5])
def test_countdown_timer_invalid_seconds_raises(bad_seconds):
    with pytest.raises(ValueError, match="seconds phải > 0"):
        CountdownTimer(seconds=bad_seconds, clock=FakeClock())


def test_start_pause_resume_and_finish():
    clock = FakeClock(now=10.0)
    timer = CountdownTimer(seconds=60.0, clock=clock)

    assert timer.running is False
    assert timer.remaining() == 60.0
    assert timer.finished() is False

    timer.start()
    assert timer.running is True

    # Gọi start() lần nữa khi đang chạy không làm reset mốc _end
    old_end = timer._end
    timer.start()
    assert timer._end == old_end

    # Trôi 25s -> còn 35s
    clock.advance(25.0)
    assert timer.remaining() == pytest.approx(35.0)

    # Tạm dừng -> dừng ở 35s, trôi thêm 20s vẫn còn 35s
    timer.pause()
    assert timer.running is False
    clock.advance(20.0)
    assert timer.remaining() == pytest.approx(35.0)

    # Chạy tiếp thêm 35s -> hoàn thành (0.0)
    timer.start()
    assert timer.running is True
    clock.advance(35.0)
    assert timer.remaining() == pytest.approx(0.0)
    assert timer.finished() is True


def test_reset_same_or_new_seconds():
    clock = FakeClock(now=0.0)
    timer = CountdownTimer(seconds=30.0, clock=clock)
    timer.start()
    clock.advance(10.0)
    timer.pause()
    assert timer.remaining() == pytest.approx(20.0)

    # Reset giữ nguyên 30s
    timer.reset()
    assert timer.running is False
    assert timer.total == 30.0
    assert timer.remaining() == 30.0

    # Reset với thời lượng mới 120s
    timer.reset(seconds=120.0)
    assert timer.total == 120.0
    assert timer.remaining() == 120.0

    # Reset với giá trị <= 0 báo ValueError
    with pytest.raises(ValueError, match="seconds phải > 0"):
        timer.reset(seconds=0)


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (0.0, "00:00"),
        (0.1, "00:01"),
        (59.0, "00:59"),
        (60.0, "01:00"),
        (61.2, "01:02"),
        (1500.0, "25:00"),
    ],
)
def test_format_mmss_ceil_behavior(seconds, expected):
    assert format_mmss(seconds) == expected