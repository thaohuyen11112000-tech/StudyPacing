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

    def test_ac2_golden_hour(self):
        sessions = [
            {"hour": 8, "completed": True},
            {"hour": 8, "completed": False},
            {"hour": 20, "completed": True},
            {"hour": 20, "completed": True},
            {"hour": 20, "completed": False},
            {"hour": 14, "completed": False},
        ]
        result = find_golden_hour(sessions)
        self.assertIsNotNone(result)
        self.assertEqual(result["hour"], 20)

    def test_build_daily_summary(self):
        summary = build_daily_summary(200, [{"hour": 9, "completed": True}])
        self.assertEqual(summary["daily_goal_minutes"], 200)
        self.assertEqual(summary["golden_hour"]["hour"], 9)


if __name__ == "__main__":
    unittest.main()
