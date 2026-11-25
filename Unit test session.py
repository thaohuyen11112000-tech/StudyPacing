import unittest

from pomodoro.config import Config, Phase
from pomodoro.session import Session


class TestSession(unittest.TestCase):
    def test_long_break_after_four(self):
        s = Session(Config())
        for _ in range(3):
            self.assertEqual(s.complete_work(), Phase.SHORT)
            s.finish_break(Phase.SHORT)
        self.assertEqual(s.complete_work(), Phase.LONG)
        self.assertTrue(s.long_due())
        s.finish_break(Phase.LONG)
        self.assertEqual(s.cycle, 0)
        self.assertEqual(s.total, 4)

    def test_abort_does_not_count(self):
        s = Session(Config())
        s.abort_work()
        self.assertEqual((s.cycle, s.total), (0, 0))

    def test_early_long_break_resets_cycle(self):
        s = Session(Config())
        s.complete_work()
        s.finish_break(Phase.LONG)  # nghỉ dài sớm do kiệt sức
        self.assertEqual(s.cycle, 0)


if __name__ == "__main__":
    unittest.main()
