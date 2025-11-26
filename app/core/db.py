from datetime import datetime, timezone

from sqlalchemy import Boolean, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql.sqltypes import DateTime

from app.core.config import settings


class Base(DeclarativeBase):
    pass


class CommonMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Уникальный идентификатор записи",
    )


class InvestmentBase(CommonMixin, Base):
    __abstract__ = True

    invested_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Собранная на текущий момент сумма",
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Флаг закрытия проекта",
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания проекта",
    )
    close_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Дата закрытия проекта",
    )


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
