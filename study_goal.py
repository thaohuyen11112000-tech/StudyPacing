class StudyGoal:
    def __init__(self):
        self.target_minutes = 0

    def set_target(self, minutes):
        if minutes <= 0:
            raise ValueError("Thời gian mục tiêu phải lớn hơn 0")
        self.target_minutes = minutes
        return True