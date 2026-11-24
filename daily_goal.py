DEFAULT_DAILY_GOAL_MINUTES = 180
MIN_DAILY_GOAL_MINUTES = 0
MAX_DAILY_GOAL_MINUTES = 1440


def is_valid_daily_goal(minutes) -> bool:
    """Kiểm tra số phút mục tiêu có nằm trong khoảng hợp lệ (0 < phút <= 1440)."""
    if isinstance(minutes, bool) or not isinstance(minutes, (int, float)):
        return False
    return MIN_DAILY_GOAL_MINUTES < minutes <= MAX_DAILY_GOAL_MINUTES