from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from .base import Base

# Связующие таблицы many-to-many
content_genre = Table(
    "content_genre",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("content_id", Integer, nullable=False),
    Column("content_type", String(20), nullable=False),
    Column("genre_id", Integer, ForeignKey("genre.id", ondelete="CASCADE")),
    UniqueConstraint("content_id", "content_type", "genre_id", name="uq_content_genre")
)

content_country = Table(
    "content_country",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("content_id", Integer, nullable=False),
    Column("content_type", String(20), nullable=False),
    Column("country_id", Integer, ForeignKey("country.id", ondelete="CASCADE")),
    UniqueConstraint("content_id", "content_type", "country_id", name="uq_content_country")
)

content_stuff = Table(
    "content_stuff",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("content_id", Integer, nullable=False),
    Column("content_type", String(20), nullable=False),
    Column("stuff_id", Integer, ForeignKey("stuff.id", ondelete="CASCADE")),
    Column("role", String(100)),  # actor, director, writer, etc.
    UniqueConstraint("content_id", "content_type", "stuff_id", "role", name="uq_content_stuff")
)
