import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.config import (
    LABELS,
    LONG_RANGE,
    SHORT_RANGE,
    WORK_RANGE,
    Config,
    Phase,
)


def test_config_defaults_and_minutes_for():
    cfg = Config()

    assert cfg.work == 25
    assert cfg.short == 5
    assert cfg.long == 15
    assert cfg.cycle == 4

    assert cfg.minutes_for(Phase.WORK) == 25
    assert cfg.minutes_for(Phase.SHORT) == 5
    assert cfg.minutes_for(Phase.LONG) == 15


def test_config_boundary_values_valid():
    cfg = Config(
        work=WORK_RANGE[1],
        short=SHORT_RANGE[1],
        long=LONG_RANGE[0],
        cycle=2,
    )
    assert cfg.work == 60
    assert cfg.short == 10
    assert cfg.long == 15
    assert cfg.cycle == 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"work": 14},
        {"work": 61},
        {"work": "25"},
        {"short": 2},
        {"short": 11},
        {"short": 5.5},
        {"long": 14},
        {"long": 31},
        {"cycle": 1},
        {"cycle": 0},
        {"cycle": "4"},
    ],
)
def test_config_invalid_values_raise_value_error(kwargs):
    with pytest.raises(ValueError):
        Config(**kwargs)


def test_phase_labels_exist():
    assert set(LABELS.keys()) == {Phase.WORK, Phase.SHORT, Phase.LONG}