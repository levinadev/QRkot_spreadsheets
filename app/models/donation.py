from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Text

from app.core.db import InvestmentBase


class Donation(InvestmentBase):
    """
    Модель, описывающая пожертвования.
    """

    __tablename__ = "donation"

    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Комментарий пользователя",
    )
    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Сумма пожертвования",
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("user.id", name="fk_donation_user_id_user"),
        nullable=True,
        comment="id пользователя",
    )
