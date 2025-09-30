from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, films, comments, users, persons, bookmarks
from .utils.db import get_conn, init_connection_pool, close_connection_pool


app = FastAPI(title="Film Base API", version="0.1.0")

# CORS (при необходимости отредактировать источники)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(films.router, prefix="/films", tags=["films"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(persons.router, prefix="/persons", tags=["persons"])
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])


@app.on_event("startup")
def startup_event():
    """Инициализация при старте приложения."""
    # Инициализируем пул соединений
    init_connection_pool()
    
    # Создаём таблицу app_user при старте, если её нет
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS app_user (
                id SERIAL PRIMARY KEY,
                email VARCHAR(320) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                is_email_verified BOOLEAN DEFAULT FALSE,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL,
                last_login_at TIMESTAMP NULL
            )
            """
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        # Если БД недоступна — сервер всё равно поднимется, но регистрация упадёт
        pass


@app.on_event("shutdown")
def shutdown_event():
    """Очистка при остановке приложения."""
    close_connection_pool()


