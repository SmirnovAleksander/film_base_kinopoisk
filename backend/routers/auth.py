from datetime import datetime, timedelta
from typing import Optional
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from ..utils.db import get_connection
from ..utils.auth import decode_token, get_current_user_id
from ..utils.mailer import send_email, send_verification_email, send_password_reset_email


router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_SECRET = "change_me"  # заменить через конфиг/переменные окружения
JWT_ALG = "HS256"
ACCESS_TTL_MIN = 15
REFRESH_TTL_DAYS = 14


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TTL_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)


def create_refresh_token(sub: str, jti: Optional[str] = None, ttl_days: int = REFRESH_TTL_DAYS) -> str:
    to_encode = {"sub": sub, "typ": "refresh"}
    if jti:
        to_encode["jti"] = jti
    expire = datetime.utcnow() + timedelta(days=ttl_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register")
def register(email: str, password: str, username: Optional[str] = None):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM app_user WHERE email=%s OR username=%s", (email, username))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Email or username already exists")
            cur.execute(
                "INSERT INTO app_user (email, username, password_hash) VALUES (%s, %s, %s) RETURNING id",
                (email, username, hash_password(password))
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return {"id": user_id, "email": email, "username": username}
        finally:
            cur.close()


@router.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, password_hash, email, username FROM app_user WHERE email=%s OR username=%s",
                        (form_data.username, form_data.username))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            user_id, password_hash_value, email, username = row
            if not verify_password(form_data.password, password_hash_value):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            access_token = create_access_token({"sub": str(user_id)})
            refresh_token = create_refresh_token(str(user_id))

            # Сохраняем refresh-токен (хэш) в БД
            ua = request.headers.get("user-agent")
            ip = request.client.host if request.client else None
            cur.execute(
                """
                INSERT INTO refresh_token(user_id, token_hash, expires_at, user_agent, ip)
                VALUES (%s, %s, NOW() + (%s)::interval, %s, %s)
                """,
                (user_id, _hash_token(refresh_token), f"{REFRESH_TTL_DAYS} days", ua, ip)
            )
            conn.commit()

            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        finally:
            cur.close()


@router.post("/refresh")
def refresh_token(refresh_token: str, request: Request):
    # В простом варианте без хранения/ревокации: проверяем тип и срок
    payload = decode_token(refresh_token)
    if payload.get("typ") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    # Проверяем токен в БД по хэшу
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id, expires_at, revoked_at
                FROM refresh_token
                WHERE user_id=%s AND token_hash=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (int(user_id), _hash_token(refresh_token))
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh not found")
            rt_id, expires_at, revoked_at = row
            if revoked_at is not None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh revoked")
            if expires_at and datetime.utcnow() > expires_at:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh expired")

            # Ротация: помечаем старый как отозванный
            cur.execute("UPDATE refresh_token SET revoked_at=NOW() WHERE id=%s", (rt_id,))

            # Выдаём новые токены и сохраняем новый refresh
            new_access = create_access_token({"sub": str(user_id)})
            new_refresh = create_refresh_token(str(user_id))
            ua = request.headers.get("user-agent")
            ip = request.client.host if request.client else None
            cur.execute(
                """
                INSERT INTO refresh_token(user_id, token_hash, expires_at, user_agent, ip)
                VALUES (%s, %s, NOW() + (%s)::interval, %s, %s)
                """,
                (int(user_id), _hash_token(new_refresh), f"{REFRESH_TTL_DAYS} days", ua, ip)
            )
            conn.commit()

            return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}
        finally:
            cur.close()


@router.post("/request-email-verify")
async def request_email_verify(user_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Получим email и username пользователя
            cur.execute("SELECT email, username FROM app_user WHERE id=%s", (user_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found")
            email, username = row

            # Генерируем токен (упрощённо)
            token = create_access_token({"sub": str(user_id)}, expires_delta=timedelta(hours=24))
            # Записываем/обновляем токен в таблице
            cur.execute(
                """
                INSERT INTO email_verification_token(user_id, token, expires_at)
                VALUES(%s, %s, NOW() + INTERVAL '24 hours')
                ON CONFLICT(user_id) DO UPDATE SET token=EXCLUDED.token, expires_at=EXCLUDED.expires_at, consumed_at=NULL
                """,
                (user_id, token)
            )
            conn.commit()
            # Отправим красивое письмо подтверждения
            sent = await send_verification_email(email, token, username)
            return {"status": "sent" if sent else "queued"}
        finally:
            cur.close()


@router.post("/verify-email")
def verify_email(token: str):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_id, expires_at, consumed_at FROM email_verification_token WHERE token=%s", (token,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Invalid token")
            user_id, expires_at, consumed_at = row
            if consumed_at is not None:
                raise HTTPException(status_code=400, detail="Already used")
            if expires_at and datetime.utcnow() > expires_at:
                raise HTTPException(status_code=400, detail="Expired token")

            # Маркируем подтверждение почты
            cur.execute("UPDATE app_user SET is_email_verified=TRUE WHERE id=%s", (user_id,))
            cur.execute("UPDATE email_verification_token SET consumed_at=NOW() WHERE token=%s", (token,))
            conn.commit()
            return {"status": "verified"}
        finally:
            cur.close()


@router.post("/request-password-reset")
async def request_password_reset(email: str):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM app_user WHERE email=%s", (email,))
            row = cur.fetchone()
            if not row:
                # Чтобы не раскрывать существование email, возвращаем 200
                return {"status": "sent"}
            user_id = row[0]
            token = create_access_token({"sub": str(user_id)}, expires_delta=timedelta(hours=1))
            cur.execute(
                """
                INSERT INTO password_reset_token(user_id, token, expires_at)
                VALUES(%s, %s, NOW() + INTERVAL '1 hour')
                ON CONFLICT(user_id) DO UPDATE SET token=EXCLUDED.token, expires_at=EXCLUDED.expires_at, consumed_at=NULL
                """,
                (user_id, token)
            )
            conn.commit()
            # Отправим красивое письмо сброса пароля
            sent = await send_password_reset_email(email, token)
            return {"status": "sent" if sent else "queued"}
        finally:
            cur.close()


@router.post("/reset-password")
def reset_password(token: str, new_password: str):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_id, expires_at, consumed_at FROM password_reset_token WHERE token=%s", (token,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Invalid token")
            user_id, expires_at, consumed_at = row
            if consumed_at is not None:
                raise HTTPException(status_code=400, detail="Already used")
            if expires_at and datetime.utcnow() > expires_at:
                raise HTTPException(status_code=400, detail="Expired token")

            cur.execute("UPDATE app_user SET password_hash=%s WHERE id=%s", (hash_password(new_password), user_id))
            cur.execute("UPDATE password_reset_token SET consumed_at=NOW() WHERE token=%s", (token,))
            conn.commit()
            return {"status": "password_changed"}
        finally:
            cur.close()


@router.post("/logout")
def logout(refresh_token: str, user_id: int = Depends(get_current_user_id)):
    """Отзывает (revoke) переданный refresh-токен текущего пользователя.

    Требует access-токен в Authorization header и сам refresh-токен в теле запроса.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE refresh_token
                SET revoked_at = NOW()
                WHERE user_id = %s AND token_hash = %s AND revoked_at IS NULL
                RETURNING id
                """,
                (user_id, _hash_token(refresh_token))
            )
            revoked = cur.rowcount
            conn.commit()
            return {"revoked": revoked}
        finally:
            cur.close()


@router.post("/logout-all")
def logout_all(user_id: int = Depends(get_current_user_id)):
    """Отзывает все активные refresh-токены текущего пользователя."""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE refresh_token
                SET revoked_at = NOW()
                WHERE user_id = %s AND revoked_at IS NULL
                """,
                (user_id,)
            )
            revoked = cur.rowcount
            conn.commit()
            return {"revoked": revoked}
        finally:
            cur.close()
