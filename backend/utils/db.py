import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from typing import Generator, Optional

from config import DATABASE_CONFIG


# Глобальный пул соединений
_connection_pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None


def init_connection_pool():
    """Инициализирует пул соединений при старте приложения."""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,      # Минимум соединений
            maxconn=20,     # Максимум соединений
            **DATABASE_CONFIG
        )


def close_connection_pool():
    """Закрывает все соединения в пуле при остановке приложения."""
    global _connection_pool
    if _connection_pool:
        _connection_pool.closeall()
        _connection_pool = None


@contextmanager
def get_connection():
    """Контекстный менеджер для получения соединения из пула."""
    if _connection_pool is None:
        init_connection_pool()
    
    conn = _connection_pool.getconn()
    try:
        yield conn
    finally:
        _connection_pool.putconn(conn)


def get_conn():
    """Функция для совместимости с Depends() - возвращает соединение из пула."""
    if _connection_pool is None:
        init_connection_pool()
    return _connection_pool.getconn()


