import unittest
from daily_goal import get_validated_daily_goal
from analytics import find_golden_hour, build_daily_summary


class TestUS04Analytics(unittest.TestCase):
    def test_ac1_daily_goal_validation(self):
        self.assertEqual(get_validated_daily_goal(None), 180)
        self.assertEqual(get_validated_daily_goal(0), 180)
        self.assertEqual(get_validated_daily_goal(-30), 180)
        self.assertEqual(get_validated_daily_goal(1500), 180)
        self.assertEqual(get_validated_daily_goal(120), 120)
        self.assertEqual(get_validated_daily_goal(1440), 1440)