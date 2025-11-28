from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

DESC_ID = "Уникальный идентификатор записи"
DESC_INVESTED_AMOUNT = "Собранная на текущий момент сумма"
DESC_FULLY_INVESTED = "Флаг закрытия проекта"
DESC_CREATE_DATE = "Дата создания проекта"
DESC_CLOSE_DATE = "Дата закрытия проекта"
EXAMPLE_ID = "1"
EXAMPLE_INVESTED_AMOUNT = "1220"
EXAMPLE_FULLY_INVESTED = "5000"
EXAMPLE_CREATE_DATE = "2025-11-15 15:42:19"
EXAMPLE_CLOSE_DATE = "2026-11-15 15:42:19"


class DBInfo(BaseModel):
    """
    Общие поля, используемые в CharityProjectDB и DonationDB
    """

    id: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": DESC_ID,
            "example": EXAMPLE_ID,
        },
    )

    invested_amount: NonNegativeInt = Field(
        0,
        json_schema_extra={
            "description": DESC_INVESTED_AMOUNT,
            "example": EXAMPLE_INVESTED_AMOUNT,
        },
    )

    fully_invested: bool = Field(
        False,
        json_schema_extra={
            "description": DESC_FULLY_INVESTED,
            "example": EXAMPLE_FULLY_INVESTED,
        },
    )

    create_date: datetime = Field(
        ...,
        json_schema_extra={
            "description": DESC_CREATE_DATE,
            "example": EXAMPLE_CREATE_DATE,
        },
    )

    close_date: datetime = Field(
        None,
        json_schema_extra={
            "description": DESC_CLOSE_DATE,
            "example": EXAMPLE_CLOSE_DATE,
        },
    )

    class Config:
        orm_mode = True
