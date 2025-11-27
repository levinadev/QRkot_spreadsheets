from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import Text

from app.core.db import InvestmentBase


class CharityProject(InvestmentBase):
    """
    Модель, описывающая целевые проекты.
    """

    __tablename__ = "charityproject"

    name: Mapped[str] = Column(
        String(100),
        unique=True,
        nullable=False,
        comment="Название проекта",
    )
    description: Mapped[str] = Column(
        Text,
        nullable=False,
        comment="Описание проекта",
    )
    full_amount: Mapped[int] = Column(
        Integer,
        nullable=False,
        comment="Целевая сумма проекта",
    )
