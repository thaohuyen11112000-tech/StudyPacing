"""Gợi ý thời gian nghỉ theo mức năng lượng (AC2).

Giữ trong khung chuẩn Pomodoro: nghỉ ngắn 3-5 phút, nghỉ dài 15-30 phút.
Mức 1 (kiệt sức) là ngoại lệ: chuyển sang nghỉ dài sớm.
"""
from dataclasses import dataclass

from .config import Phase

LEVELS = {
    1: "Kiệt sức",
    2: "Mệt",
    3: "Bình thường",
    4: "Tốt",
    5: "Tràn năng lượng",
}

_SHORT = {5: 3, 4: 4, 3: 5, 2: 5, 1: 15}
_LONG = {5: 15, 4: 15, 3: 20, 2: 25, 1: 30}

_SHORT_WHY = {
    1: "Bạn đang kiệt sức: nên nghỉ dài ngay thay vì nghỉ ngắn.",
    2: "Bạn hơi mệt: nghỉ ngắn tối đa 5 phút, đứng dậy vận động nhẹ.",
    3: "Mức bình thường: nghỉ ngắn 5 phút theo chuẩn.",
    4: "Năng lượng tốt: nghỉ ngắn 4 phút là đủ.",
    5: "Năng lượng tràn đầy: nghỉ ngắn 3 phút để giữ đà học.",
}
_LONG_WHY = {
    1: "Rất mệt: nghỉ dài tối đa, rời màn hình, đi lại và uống nước.",
    2: "Khá mệt: nên nghỉ dài hơn để phục hồi.",
    3: "Bình thường: nghỉ dài vừa phải.",
    4: "Năng lượng tốt: nghỉ dài ở mức tối thiểu là đủ.",
    5: "Năng lượng tràn đầy: nghỉ dài ở mức tối thiểu.",
}


@dataclass(frozen=True)
class Suggestion:
    phase: Phase
    minutes: int
    reason: str


def suggest_break(level: int, long_due: bool) -> Suggestion:
    """level: 1-5. long_due: True nếu đã đủ số phiên để nghỉ dài."""
    if level not in LEVELS:
        raise ValueError("level phải là số nguyên từ 1 đến 5")
    if long_due:
        return Suggestion(Phase.LONG, _LONG[level], _LONG_WHY[level])
    phase = Phase.LONG if level == 1 else Phase.SHORT
    return Suggestion(phase, _SHORT[level], _SHORT_WHY[level])
