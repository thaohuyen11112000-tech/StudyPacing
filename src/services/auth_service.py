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
   
    def register(self, email: str, password: str, full_name: str = "") -> dict:
        if not email or not password:
            return {"success": False, "error": "Email và mật khẩu không được để trống."}

        email_chuan = email.strip().lower()
        if not self._kiem_tra_email_hop_le(email_chuan):
            return {"success": False, "error": "Định dạng email không hợp lệ."}

        if len(password) < 6:
            return {"success": False, "error": "Mật khẩu phải có ít nhất 6 ký tự."}

        if email_chuan in self._users_by_email:
            return {"success": False, "error": "Email này đã được sử dụng."}

        user_id = str(uuid.uuid4())
        mat_khau_ma_hoa = generate_password_hash(password)

        self._users_by_email[email_chuan] = {
            "id": user_id,
            "email": email_chuan,
            "full_name": full_name.strip(),
            "password_hash": mat_khau_ma_hoa,
        }

        return {
            "success": True,
            "message": "Đăng ký tài khoản thành công.",
            "user": {
                "id": user_id,
                "email": email_chuan,
                "full_name": full_name.strip(),
            },
        }

    def login(self, email: str, password: str) -> dict:
        if not email or not password:
            return {"success": False, "error": "Vui lòng nhập đầy đủ email và mật khẩu."}

        email_chuan = email.strip().lower()
        nguoi_dung = self._users_by_email.get(email_chuan)

        if not nguoi_dung or not check_password_hash(nguoi_dung["password_hash"], password):
            return {"success": False, "error": "Email hoặc mật khẩu không chính xác."}

        token = secrets.token_urlsafe(32)
        self._sessions[token] = {
            "user_id": nguoi_dung["id"],
            "email": nguoi_dung["email"],
        }

        return {
            "success": True,
            "message": "Đăng nhập thành công.",
            "token": token,
            "session": {
                "token": token,
                "user_id": nguoi_dung["id"],
                "email": nguoi_dung["email"],
            },
            "user": {
                "id": nguoi_dung["id"],
                "email": nguoi_dung["email"],
                "full_name": nguoi_dung["full_name"],
            },
        }

    def verify_session(self, token: str) -> dict | None:
        if not token:
            return None
        return self._sessions.get(token)

    def logout(self, token: str) -> bool:
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False