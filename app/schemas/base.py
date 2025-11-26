from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt


class DBInfo(BaseModel):
    """
    Общие поля, используемые в CharityProjectDB и DonationDB
    """

    id: Annotated[
        PositiveInt,
        Field(
            json_schema_extra={
                "description": "Уникальный идентификатор записи",
                "example": "1",
            },
        ),
    ]

    invested_amount: Annotated[
        NonNegativeInt,
        Field(
            0,
            json_schema_extra={
                "description": "Собранная на текущий момент сумма",
                "example": "1220",
            },
        ),
    ]

    fully_invested: Annotated[
        bool,
        Field(
            False,
            json_schema_extra={
                "description": "Флаг закрытия проекта",
                "example": "5000",
            },
        ),
    ]

    create_date: Annotated[
        datetime,
        Field(
            json_schema_extra={
                "description": "Дата создания проекта",
                "example": "2025-11-15 15:42:19",
            },
        ),
    ]

    close_date: Annotated[
        datetime,
        Field(
            json_schema_extra={
                "description": "Дата закрытия проекта",
                "example": "2026-11-15 15:42:19",
            },
        ),
    ]

    model_config = ConfigDict(from_attributes=True)
