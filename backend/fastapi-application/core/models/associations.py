from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from .base import Base

# Связи many-to-many

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("film_id", Integer, ForeignKey("film.id", ondelete="CASCADE")),
    Column("genre_id", Integer, ForeignKey("genre.id", ondelete="CASCADE")),
    UniqueConstraint("film_id", "genre_id", name="uq_film_genre")
)

film_country = Table(
    "film_country",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("film_id", Integer, ForeignKey("film.id", ondelete="CASCADE")),
    Column("country_id", Integer, ForeignKey("country.id", ondelete="CASCADE")),
    UniqueConstraint("film_id", "country_id", name="uq_film_country")
)

film_stuff = Table(
    "film_stuff",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("film_id", Integer, ForeignKey("film.id", ondelete="CASCADE")),
    Column("stuff_id", Integer, ForeignKey("stuff.id", ondelete="CASCADE")),
    Column("role", String(100)),  # actor, director, writer, etc.
    UniqueConstraint("film_id", "stuff_id", "role", name="uq_film_stuff")
)
