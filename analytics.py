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