def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return task

    print("Khong tim thay task!")
    return None
    