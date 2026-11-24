DEFAULT_DAILY_GOAL_MINUTES = 180
MIN_DAILY_GOAL_MINUTES = 0
MAX_DAILY_GOAL_MINUTES = 1440


def is_valid_daily_goal(minutes) -> bool:
    """Kiểm tra số phút mục tiêu có nằm trong khoảng hợp lệ (0 < phút <= 1440)."""
    if isinstance(minutes, bool) or not isinstance(minutes, (int, float)):
        return False
    return MIN_DAILY_GOAL_MINUTES < minutes <= MAX_DAILY_GOAL_MINUTES

def get_validated_daily_goal(minutes=None):
    """Trả về số phút mục tiêu hợp lệ, mặc định 180 phút/ngày nếu không hợp lệ."""
    if minutes is None or not is_valid_daily_goal(minutes):
        return DEFAULT_DAILY_GOAL_MINUTES
    if isinstance(minutes, float) and minutes.is_integer():
        return int(minutes)
    return minutes