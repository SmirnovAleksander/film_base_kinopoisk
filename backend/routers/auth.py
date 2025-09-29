from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from ..utils.db import get_conn


router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_SECRET = "change_me"  # заменить через конфиг/переменные окружения
JWT_ALG = "HS256"
ACCESS_TTL_MIN = 15


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TTL_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register")
def register(email: str, password: str, username: Optional[str] = None, conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM users WHERE email=%s OR username=%s", (email, username))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email or username already exists")
        cur.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s) RETURNING id",
            (email, username, hash_password(password))
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return {"id": user_id, "email": email, "username": username}
    finally:
        cur.close()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, password_hash, email, username FROM users WHERE email=%s OR username=%s",
                    (form_data.username, form_data.username))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        user_id, password_hash_value, email, username = row
        if not verify_password(form_data.password, password_hash_value):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token({"sub": str(user_id)})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        cur.close()


