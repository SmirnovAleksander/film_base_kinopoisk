from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .associations import content_country

if TYPE_CHECKING:
    from .film import Film
    from .series import Series


class Country(Base, IntIdPkMixin):
    """Модель страны"""
    __tablename__ = "country"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary=content_country,
        primaryjoin="and_(Country.id==foreign(content_country.c.country_id), content_country.c.content_type=='film')",
        secondaryjoin="Film.id==foreign(content_country.c.content_id)",
        back_populates="countries",
        overlaps="series,countries"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_country,
        primaryjoin="and_(Country.id==foreign(content_country.c.country_id), content_country.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_country.c.content_id)",
        back_populates="countries",
        overlaps="films,countries"
    )
