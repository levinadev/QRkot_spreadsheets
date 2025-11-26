from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import DBInfo


class DonationBase(BaseModel):
    """
    Базовая схема пожертвования
    """

    full_amount: Annotated[
        PositiveInt,
        Field(
            json_schema_extra={
                "description": "Сумма пожертвования",
                "example": 500,
            }
        ),
    ]

    comment: Annotated[
        Optional[str],
        Field(
            default=None,
            json_schema_extra={
                "description": "Комментарий пользователя",
                "example": "На помощь котикам",
            },
        ),
    ]


class DonationCreate(DonationBase):
    """
    Схема запроса для создания пожертвования
    """

    model_config = {"extra": "forbid"}


class DonationDB(DBInfo, DonationBase):
    """
    Схема ответа, описывает возвращаемый из БД объект
    """

    user_id: Annotated[
        PositiveInt,
        Field(
            json_schema_extra={
                "description": "Уникальный идентификатор записи",
                "example": "1",
            },
        ),
    ]


class DonationCreateResponse(DonationBase):
    """
    Схема ответа для создания пожертвования
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

    create_date: Annotated[
        datetime,
        Field(
            json_schema_extra={
                "description": "Дата создания проекта",
                "example": "2025-11-15 15:42:19",
            },
        ),
    ]


class DonationUserResponse(DonationCreateResponse):
    """
    Схема ответа для списка пожертвований пользователя.
    """

    model_config = {"from_attributes": True}
