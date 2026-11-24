def add_task(tasks, title, description, deadline, status, priority):
    if priority not in ["High", "Medium", "Low"]:
        print("Muc do uu tien khong hop le!")
        return

    if tasks:
        task_id = max(task["id"] for task in tasks) + 1
    else:
        task_id = 1

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "deadline": deadline,
        "status": status,
        "priority": priority
    }

    tasks.append(task)
    print("Them bai tap thanh cong!")
    