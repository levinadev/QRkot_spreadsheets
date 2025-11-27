from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.sqltypes import Text

from app.core.db import InvestmentBase


class Donation(InvestmentBase):
    """
    Модель, описывающая пожертвования.
    """

    __tablename__ = "donation"

    comment: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
        comment="Комментарий пользователя",
    )
    full_amount: Mapped[int] = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Сумма пожертвования",
    )
    user_id: Mapped[Optional[int]] = Column(
        Integer,
        ForeignKey("user.id", name="fk_donation_user_id_user"),
        nullable=True,
        comment="id пользователя",
    )
