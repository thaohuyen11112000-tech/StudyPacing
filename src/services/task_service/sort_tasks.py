PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def classify_tasks(tasks):
    groups = {"High": [], "Medium": [], "Low": []}

    for task in tasks:
        priority = task.get("priority")
        if priority in groups:
            groups[priority].append(task)

    return groups


def sort_tasks(tasks):
    return sorted(
        tasks,
        key=lambda task: (
            PRIORITY_ORDER.get(task.get("priority"), len(PRIORITY_ORDER)),
            task.get("deadline") or "9999-12-31",
        ),
    )
    