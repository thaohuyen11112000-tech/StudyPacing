class TaskManager:
    def __init__(self, tasks=None):
        """
        Khởi tạo TaskManager với danh sách tasks tuân thủ quy ước:
        {"title": "Tên bài học", "priority": "Cao/Trung bình/Thấp", "completed": True/False}
        """
        self.tasks = tasks if tasks is not None else []

    def add_task(self, title, priority="Trung bình"):
        """Thêm một công việc mới vào danh sách."""
        new_task = {
            "title": title,
            "priority": priority,
            "completed": False,  # Mặc định chưa hoàn thành
            "status": "Chưa xong" # Hỗ trợ tương thích biến status nếu các module khác cần
        }
        self.tasks.append(new_task)
        print(f"✅ Đã thêm task thành công: '{title}' (Ưu tiên: {priority})")

    def complete_task(self, index):
        """Đánh dấu hoàn thành công việc theo số thứ tự (index từ 0)."""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.tasks[index]["status"] = "Done"  # Đồng bộ theo chuẩn status: Done
            print(f"🎉 Đã hoàn thành task: '{self.tasks[index]['title']}'")
        else:
            print("❌ Lỗi: Số thứ tự công việc không hợp lệ!")

    def get_all_tasks(self):
        """Trả về danh sách tasks để module khác (như analytics.py hoặc storage.py) đọc."""
        return self.tasks

    def print_tasks(self):
        """Hiển thị danh sách công việc ra màn hình một cách trực quan."""
        if not self.tasks:
            print("📭 Danh sách công việc hiện đang trống.")
            return

        print("\n================ DANH SÁCH CÔNG VIỆC ================")
        for i, task in enumerate(self.tasks):
            # Xử lý linh hoạt đọc trạng thái từ 'completed' hoặc 'status'
            is_completed = (
                task.get("completed", False) or 
                task.get("status") in ["Done", "Hoàn thành", True]
            )
            status_str = "[X] Đã hoàn thành" if is_completed else "[ ] Chưa hoàn thành"
            
            title = task.get("title", "Không có tên")
            priority = task.get("priority", "Trung bình")
            
            print(f"{i + 1}. {title} | Ưu tiên: {priority} | Trạng thái: {status_str}")
        print("======================================================")


# --- Khối kiểm thử độc lập (Test thử module) ---
if __name__ == "__main__":
    manager = TaskManager()
    
    # Thêm thử vài task mẫu
    manager.add_task("Học lập trình Git nâng cao", "Cao")
    manager.add_task("Làm bài tập nhóm môn CNPM", "Trung bình")
    
    # Hiển thị danh sách
    manager.print_tasks()
    
    # Đánh dấu hoàn thành task đầu tiên
    manager.complete_task(0)
    
    # Xem lại danh sách sau khi cập nhật trạng thái
    manager.print_tasks()