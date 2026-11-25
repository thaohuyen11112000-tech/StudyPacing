import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.config import Config, Phase
from src.services.session import Session


def test_session_initial_state():
    cfg = Config(cycle=4)
    session = Session(cfg)

    assert session.cycle == 0
    assert session.total == 0
    assert session.long_due() is False


def test_complete_work_cycle_and_reset_on_long_break():
    cfg = Config(cycle=3)
    session = Session(cfg)

    assert session.complete_work() == Phase.SHORT
    assert (session.cycle, session.total) == (1, 1)

    assert session.complete_work() == Phase.SHORT
    assert (session.cycle, session.total) == (2, 2)
    session.finish_break(Phase.SHORT)
    assert session.cycle == 2

    assert session.complete_work() == Phase.LONG
    assert (session.cycle, session.total) == (3, 3)
    assert session.long_due() is True

    session.finish_break(Phase.LONG)
    assert session.cycle == 0
    assert session.total == 3
    assert session.long_due() is False


def test_abort_work_does_not_count():
    cfg = Config(cycle=4)
    session = Session(cfg)

    session.complete_work()
    session.abort_work()

    assert session.cycle == 1
    assert session.total == 1