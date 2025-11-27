from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, sessionmaker
from sqlalchemy.sql.sqltypes import DateTime

from app.core.config import settings

Base = declarative_base()


class CommonMixin:
    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        comment="Уникальный идентификатор записи",
    )


class InvestmentBase(CommonMixin, Base):
    __abstract__ = True

    invested_amount: Mapped[str] = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Собранная на текущий момент сумма",
    )
    fully_invested: Mapped[bool] = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Флаг закрытия проекта",
    )
    create_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания проекта",
    )
    close_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата закрытия проекта",
    )


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
