import re
import secrets
import uuid
from werkzeug.security import check_password_hash, generate_password_hash


class AuthService:
    def __init__(self):
        # Lưu tạm người dùng và phiên đăng nhập trong bộ nhớ ở Sprint 1
        self._users_by_email = {}
        self._sessions = {}

    def _kiem_tra_email_hop_le(self, email: str) -> bool:
        mau_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return bool(email and re.match(mau_email, email.strip()))