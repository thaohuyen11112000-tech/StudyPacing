import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.auth_service import AuthService


def test_register_success_and_hash_password():
    auth = AuthService()
    res = auth.register("User@Example.com", "matkhau123", "Nguyen Van A")

    assert res["success"] is True
    assert res["user"]["email"] == "user@example.com"
    assert res["user"]["full_name"] == "Nguyen Van A"
    saved_user = auth._users_by_email["user@example.com"]
    assert saved_user["password_hash"] != "matkhau123"


@pytest.mark.parametrize(
    "email,password",
    [
        ("", "123456"),
        ("user@example.com", ""),
        ("email-sai-dinh-dang", "123456"),
        ("user@example.com", "12345"),
    ],
)
def test_register_invalid_inputs(email, password):
    auth = AuthService()
    res = auth.register(email, password)
    assert res["success"] is False
    assert "error" in res


def test_register_duplicate_email():
    auth = AuthService()
    auth.register("test@gmail.com", "123456")
    res = auth.register("TEST@gmail.com", "654321")

    assert res["success"] is False
    assert "đã được sử dụng" in res["error"]


def test_login_verify_and_logout_flow():
    auth = AuthService()
    auth.register("hocvien@gmail.com", "secret123", "Hoc Vien")

    login_res = auth.login("hocvien@gmail.com", "secret123")
    assert login_res["success"] is True
    token = login_res["token"]

    session_info = auth.verify_session(token)
    assert session_info is not None
    assert session_info["email"] == "hocvien@gmail.com"

    assert auth.logout(token) is True
    assert auth.verify_session(token) is None
    assert auth.logout(token) is False


def test_login_wrong_credentials():
    auth = AuthService()
    auth.register("hocvien@gmail.com", "secret123")

    assert auth.login("hocvien@gmail.com", "sai_pass")["success"] is False
    assert auth.login("khong_ton_tai@gmail.com", "secret123")["success"] is False
    assert auth.login("", "")["success"] is False