import pytest
from datetime import timedelta, datetime, timezone
from unittest.mock import MagicMock
from fastapi import HTTPException
import jwt

from app.services import auth_service
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def test_hash_and_verify_password():
    password = "mysecret"
    hashed = auth_service.hash_password(password)
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrongpassword", hashed)

def test_create_and_decode_access_token():
    data = {"sub": "user@test.com"}
    token = auth_service.create_access_token(data, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "user@test.com"
    assert "exp" in decoded

def test_create_and_verify_reset_token():
    email = "user@test.com"
    token = auth_service.create_reset_token(email, expires_minutes=1)
    result = auth_service.verify_reset_token(token)
    assert result == email

def test_verify_reset_token_expired(monkeypatch):
    email = "user@test.com"
    token = auth_service.create_reset_token(email, expires_minutes=-1)
    with pytest.raises(HTTPException) as exc_info:
        auth_service.verify_reset_token(token)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Token expired"

def test_verify_reset_token_invalid():
    with pytest.raises(HTTPException) as exc_info:
        auth_service.verify_reset_token("invalidtoken")
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid token"

def test_reset_password_success():
    db = MagicMock()
    fake_user = MagicMock()
    token = auth_service.create_reset_token("user@test.com")
    
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(auth_service, "verify_reset_token", lambda t: "user@test.com")
    monkeypatch.setattr(auth_service, "get_user_by_email", lambda db, email: fake_user)
    monkeypatch.setattr(auth_service, "update_user_password", lambda db, user, hashed: True)

    result = auth_service.reset_password(db, token, "newpassword")
    assert result["msg"] == "Password updated successfully"

def test_reset_password_user_not_found(monkeypatch):
    db = MagicMock()
    token = auth_service.create_reset_token("user@test.com")
    
    monkeypatch.setattr(auth_service, "verify_reset_token", lambda t: "user@test.com")
    monkeypatch.setattr(auth_service, "get_user_by_email", lambda db, email: None)

    with pytest.raises(HTTPException) as exc_info:
        auth_service.reset_password(db, token, "newpassword")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
