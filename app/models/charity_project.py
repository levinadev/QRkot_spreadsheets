from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Text

from app.core.db import InvestmentBase


class CharityProject(InvestmentBase):
    """
    Модель, описывающая целевые проекты.
    """

    __tablename__ = "charityproject"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="Название проекта",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Описание проекта",
    )
    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Целевая сумма проекта",
    )
