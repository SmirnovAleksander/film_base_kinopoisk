from datetime import datetime
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from .db import get_connection

JWT_SECRET = "change_me"  # вынести в config.py при необходимости
JWT_ALG = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    try:
        return int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid subject in token")


def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    """Получает роль текущего пользователя из токена"""
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT role FROM app_user WHERE id = %s", (user_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return result[0]
        finally:
            cur.close()


def require_role(allowed_roles: List[str]):
    """Декоратор для проверки ролей пользователя"""
    def role_checker(current_role: str = Depends(get_current_user_role)):
        if current_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_role
    return role_checker


def require_admin():
    """Проверяет, что пользователь является администратором"""
    return require_role(["admin"])


def require_moderator():
    """Проверяет, что пользователь является модератором или администратором"""
    return require_role(["moderator", "admin"])


def require_user():
    """Проверяет, что пользователь авторизован (любая роль)"""
    return require_role(["user", "moderator", "admin"])


