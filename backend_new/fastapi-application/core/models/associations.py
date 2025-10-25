from sqlalchemy import Table, Column, Integer, String, ForeignKey
from .base import Base

# Связующие таблицы many-to-many

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

film_country = Table(
    "film_country", 
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True),
    Column("country_id", Integer, ForeignKey("countries.id", ondelete="CASCADE"), primary_key=True),
)

film_stuff = Table(
    "film_stuff",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id", ondelete="CASCADE"), primary_key=True),
    Column("stuff_id", Integer, ForeignKey("stuff.id", ondelete="CASCADE"), primary_key=True),
    Column("role", String(100)),  # actor, director, writer, etc.
)
