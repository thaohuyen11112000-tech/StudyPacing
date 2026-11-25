import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.config import Phase
from src.services.energy import LEVELS, Suggestion, _LONG, _SHORT, suggest_break


@pytest.mark.parametrize("level", [1, 2, 3, 4, 5])
def test_suggest_break_long_due_all_levels(level):
    res = suggest_break(level=level, long_due=True)

    assert isinstance(res, Suggestion)
    assert res.phase == Phase.LONG
    assert res.minutes == _LONG[level]
    assert isinstance(res.reason, str) and len(res.reason) > 0


@pytest.mark.parametrize("level", [2, 3, 4, 5])
def test_suggest_break_short_break_normal_levels(level):
    res = suggest_break(level=level, long_due=False)

    assert res.phase == Phase.SHORT
    assert res.minutes == _SHORT[level]
    assert 3 <= res.minutes <= 5


def test_suggest_break_level_1_exhausted_forces_long_break():
    res = suggest_break(level=1, long_due=False)

    assert res.phase == Phase.LONG
    assert res.minutes == _SHORT[1]
    assert "kiệt sức" in res.reason.lower()


@pytest.mark.parametrize("invalid_level", [0, -1, 6, 99, "3", None])
def test_suggest_break_invalid_level_raises_value_error(invalid_level):
    with pytest.raises(ValueError, match="1 đến 5"):
        suggest_break(level=invalid_level, long_due=False)


def test_levels_mapping_complete():
    assert set(LEVELS.keys()) == {1, 2, 3, 4, 5}