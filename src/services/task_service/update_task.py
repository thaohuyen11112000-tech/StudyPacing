def update_task(tasks, task_id, title=None, description=None,
                deadline=None, status=None, priority=None):
    if priority is not None and priority not in ["High", "Medium", "Low"]:
        print("Muc do uu tien khong hop le!")
        return None

    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if deadline is not None:
                task["deadline"] = deadline
            if status is not None:
                task["status"] = status
            if priority is not None:
                task["priority"] = priority
            return task

    print("Khong tim thay task!")
    return None
    