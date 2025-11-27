from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class DBInfo(BaseModel):
    """
    Общие поля, используемые в CharityProjectDB и DonationDB
    """

    id: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": "Уникальный идентификатор записи",
            "example": "1",
        },
    )

    invested_amount: NonNegativeInt = Field(
        0,
        json_schema_extra={
            "description": "Собранная на текущий момент сумма",
            "example": "1220",
        },
    )

    fully_invested: bool = Field(
        False,
        json_schema_extra={
            "description": "Флаг закрытия проекта",
            "example": "5000",
        },
    )

    create_date: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Дата создания проекта",
            "example": "2025-11-15 15:42:19",
        },
    )

    close_date: datetime = Field(
        None,
        json_schema_extra={
            "description": "Дата закрытия проекта",
            "example": "2026-11-15 15:42:19",
        },
    )

    class Config:
        orm_mode = True
