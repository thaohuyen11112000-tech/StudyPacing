from daily_goal import get_validated_daily_goal


def analyze_hourly_completion(sessions: list[dict]) -> dict[int, dict]:
    """Thống kê số phiên hoàn thành, tổng số phiên và tỷ lệ hoàn thành theo từng giờ (0-23)."""
    hourly_stats: dict[int, dict] = {}

    for session in sessions or []:
        hour = session.get("hour", session.get("start_hour"))
        if not isinstance(hour, int) or not (0 <= hour <= 23):
            continue

        if hour not in hourly_stats:
            hourly_stats[hour] = {"completed": 0, "total": 0, "rate": 0.0}

        hourly_stats[hour]["total"] += 1
        if bool(session.get("completed", False)):
            hourly_stats[hour]["completed"] += 1

    for hour, stat in hourly_stats.items():
        stat["rate"] = stat["completed"] / stat["total"] if stat["total"] > 0 else 0.0

    return hourly_stats

def find_golden_hour(sessions: list[dict]) -> dict | None:
    """Tìm khung giờ có tỷ lệ hoàn thành phiên học cao nhất."""
    hourly_stats = analyze_hourly_completion(sessions)
    if not hourly_stats:
        return None

    best_hour = None
    best_rate = -1.0
    best_completed = -1

    for hour in sorted(hourly_stats.keys()):
        completed = hourly_stats[hour]["completed"]
        rate = hourly_stats[hour]["rate"]

        if (rate > best_rate) or (rate == best_rate and completed > best_completed):
            best_rate = rate
            best_completed = completed
            best_hour = hour

    return {
        "hour": best_hour,
        "time_range": f"{best_hour:02d}:00 - {best_hour + 1:02d}:00",
        "completion_rate": round(best_rate, 4),
        "completed": best_completed,
        "total": hourly_stats[best_hour]["total"],
    }


def build_daily_summary(goal_minutes, sessions: list[dict]) -> dict:
    """Tổng hợp mục tiêu ngày hợp lệ (AC1) và khung giờ vàng (AC2)."""
    return {
        "daily_goal_minutes": get_validated_daily_goal(goal_minutes),
        "golden_hour": find_golden_hour(sessions),
    }
def find_golden_hour(sessions: list[dict]) -> dict | None:
    """Tìm khung giờ có tỷ lệ hoàn thành phiên học cao nhất."""
    hourly_stats = analyze_hourly_completion(sessions)
    if not hourly_stats:
        return None

    best_hour = None
    best_rate = -1.0
    best_completed = -1

    for hour in sorted(hourly_stats.keys()):
        completed = hourly_stats[hour]["completed"]
        rate = hourly_stats[hour]["rate"]

        if (rate > best_rate) or (rate == best_rate and completed > best_completed):
            best_rate = rate
            best_completed = completed
            best_hour = hour

    return {
        "hour": best_hour,
        "time_range": f"{best_hour:02d}:00 - {best_hour + 1:02d}:00",
        "completion_rate": round(best_rate, 4),
        "completed": best_completed,
        "total": hourly_stats[best_hour]["total"],
    }


def build_daily_summary(goal_minutes, sessions: list[dict]) -> dict:
    """Tổng hợp mục tiêu ngày hợp lệ (AC1) và khung giờ vàng (AC2)."""
    return {
        "daily_goal_minutes": get_validated_daily_goal(goal_minutes),
        "golden_hour": find_golden_hour(sessions),
    }