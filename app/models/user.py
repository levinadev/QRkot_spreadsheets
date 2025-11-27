from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель, описывающая пользователя.
    """

    id: Mapped[int] = Column(Integer, primary_key=True)
