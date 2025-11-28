from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import DBInfo

DESC_FULL_AMOUNT = "Сумма пожертвования"
DESC_COMMENT = "Комментарий пользователя"
DESC_USER_ID = "Уникальный идентификатор пользователя"
DESC_ID = "Уникальный идентификатор записи"
DESC_CREATE_DATE = "Дата создания проекта"
EXAMPLE_FULL_AMOUNT = 500
EXAMPLE_COMMENT = "На помощь котикам"
EXAMPLE_USER_ID = "1"
EXAMPLE_ID = "1"
EXAMPLE_CREATE_DATE = "2025-11-15 15:42:19"


class DonationBase(BaseModel):
    """
    Базовая схема пожертвования
    """

    full_amount: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": DESC_FULL_AMOUNT,
            "example": EXAMPLE_FULL_AMOUNT,
        },
    )

    comment: Optional[str] = Field(
        None,
        json_schema_extra={
            "description": DESC_COMMENT,
            "example": EXAMPLE_COMMENT,
        },
    )


class DonationCreate(DonationBase):
    """
    Схема запроса для создания пожертвования
    """

    class Config:
        extra = "forbid"


class DonationDB(DBInfo, DonationBase):
    """
    Схема ответа, описывает возвращаемый из БД объект
    """

    user_id: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": DESC_USER_ID,
            "example": EXAMPLE_USER_ID,
        },
    )


class DonationCreateResponse(DonationBase):
    """
    Схема ответа для создания пожертвования
    """

    id: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": DESC_ID,
            "example": EXAMPLE_ID,
        },
    )

    create_date: datetime = Field(
        ...,
        json_schema_extra={
            "description": DESC_CREATE_DATE,
            "example": EXAMPLE_CREATE_DATE,
        },
    )

    class Config:
        orm_mode = True


class DonationUserResponse(DonationCreateResponse):
    """
    Схема ответа для списка пожертвований пользователя.
    """

    class Config:
        from_attributes = True
