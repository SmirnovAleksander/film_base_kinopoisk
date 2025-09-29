import psycopg2
from contextlib import contextmanager
from typing import Generator

from config import DATABASE_CONFIG


def get_conn():
    return psycopg2.connect(**DATABASE_CONFIG)


