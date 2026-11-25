"""Quản lý chu kỳ Pomodoro: đếm phiên, quyết định khi nào nghỉ dài."""
from .config import Config, Phase


class Session:
    def __init__(self, config: Config):
        self.config = config
        self.cycle = 0   # số phiên đã xong trong chu kỳ hiện tại
        self.total = 0   # tổng số Pomodoro hoàn thành

    def long_due(self) -> bool:
        return self.cycle >= self.config.cycle

    def complete_work(self) -> Phase:
        """Ghi nhận một Pomodoro hoàn chỉnh; trả về loại nghỉ mặc định kế tiếp."""
        self.cycle += 1
        self.total += 1
        return Phase.LONG if self.long_due() else Phase.SHORT

    def abort_work(self) -> None:
        """Phiên bị hủy giữa chừng: không được tính là Pomodoro."""

    def finish_break(self, phase: Phase) -> None:
        if phase == Phase.LONG:
            self.cycle = 0
