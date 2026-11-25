"""Cấu hình và kiểm tra hợp lệ theo khung chuẩn Pomodoro."""
from dataclasses import dataclass
from enum import Enum

WORK_RANGE = (15, 60)    # AC1: tùy chỉnh 15-60 phút
SHORT_RANGE = (3, 10)    # nghỉ ngắn chuẩn: 3-5 phút (cho phép tới 10)
LONG_RANGE = (15, 30)    # nghỉ dài chuẩn: 15-30 phút


class Phase(str, Enum):
    WORK = "work"
    SHORT = "short"
    LONG = "long"


LABELS = {
    Phase.WORK: "Tập trung học",
    Phase.SHORT: "Nghỉ ngắn",
    Phase.LONG: "Nghỉ dài",
}


@dataclass
class Config:
    work: int = 25
    short: int = 5
    long: int = 15
    cycle: int = 4  # số phiên học trước khi nghỉ dài

    def __post_init__(self):
        self.validate()

    def validate(self):
        for name, (lo, hi) in (
            ("work", WORK_RANGE),
            ("short", SHORT_RANGE),
            ("long", LONG_RANGE),
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or not lo <= value <= hi:
                raise ValueError(f"{name} phải là số nguyên trong khoảng {lo}-{hi} phút (nhận {value!r})")
        if not isinstance(self.cycle, int) or self.cycle < 2:
            raise ValueError("cycle phải là số nguyên >= 2")

    def minutes_for(self, phase: Phase) -> int:
        return {Phase.WORK: self.work, Phase.SHORT: self.short, Phase.LONG: self.long}[phase]
