import sqlite3

class StudyPlan:
    def __init__(self, id, subject_name, target_hours, deadline):
        self.id = id
        self.subject_name = subject_name
        self.target_hours = target_hours
        self.deadline = deadline

class StudyPlanRepository:
    def __init__(self, db_name="studypacing.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Khởi tạo bảng StudyPlan trong CSDL SQLite"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT UNIQUE NOT NULL,
                target_hours REAL NOT NULL,
                deadline TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, study_plan):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO study_plans (subject_name, target_hours, deadline)
            VALUES (?, ?, ?)
        ''', (study_plan.subject_name, study_plan.target_hours, study_plan.deadline))
        conn.commit()
        conn.close()

    def find_by_subject(self, subject_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM study_plans WHERE subject_name = ?', (subject_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return StudyPlan(id=row[0], subject_name=row[1], target_hours=row[2], deadline=row[3])
        return None