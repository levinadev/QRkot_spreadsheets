from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import DBInfo

NAME_MIN_LENGTH = 5
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 10
DESC_NAME = "Название проекта"
DESC_DESCRIPTION = "Описание проекта"
DESC_FULL_AMOUNT = "Целевая сумма проекта"
EXAMPLE_NAME = "Помощь котикам"
EXAMPLE_DESCRIPTION = "На корм для котиков"
EXAMPLE_FULL_AMOUNT_CREATE = "1000"
EXAMPLE_FULL_AMOUNT_UPDATE = "2000"


class CharityProjectBase(BaseModel):
    """
    Базовая схема проекта
    """

    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        json_schema_extra={
            "description": DESC_NAME,
            "example": EXAMPLE_NAME,
        },
    )

    description: str = Field(
        ...,
        min_length=DESCRIPTION_MIN_LENGTH,
        json_schema_extra={
            "description": DESC_DESCRIPTION,
            "example": EXAMPLE_DESCRIPTION,
        },
    )

    full_amount: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": DESC_FULL_AMOUNT,
            "example": EXAMPLE_FULL_AMOUNT_CREATE,
        },
    )


class CharityProjectCreate(CharityProjectBase):
    """
    Схема запроса для создания проекта
    """
    class Config:
        extra = "forbid"


class CharityProjectDB(DBInfo, CharityProjectBase):
    """
    Схема ответа, описывает возвращаемый из БД объект
    """


class CharityProjectUpdate(BaseModel):
    """
    Схема запроса для обновления
    """

    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        json_schema_extra={
            "description": DESC_NAME,
            "example": EXAMPLE_NAME,
        },
    )

    description: Optional[str] = Field(
        None,
        min_length=DESCRIPTION_MIN_LENGTH,
        json_schema_extra={
            "description": DESC_DESCRIPTION,
            "example": EXAMPLE_DESCRIPTION,
        },
    )

    full_amount: Optional[PositiveInt] = Field(
        None,
        json_schema_extra={
            "description": DESC_FULL_AMOUNT,
            "example": EXAMPLE_FULL_AMOUNT_UPDATE,
        },
    )

    class Config:
        extra = "forbid"
