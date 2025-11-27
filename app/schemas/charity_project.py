from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import DBInfo


class CharityProjectBase(BaseModel):
    """
    Базовая схема проекта
    """

    name: str = Field(
        ...,
        min_length=5,
        max_length=100,
        json_schema_extra={
            "description": "Название проекта",
            "example": "Помощь котикам",
        },
    )

    description: str = Field(
        ...,
        min_length=10,
        json_schema_extra={
            "description": "Описание проекта",
            "example": "На корм для котиков",
        },
    )

    full_amount: PositiveInt = Field(
        ...,
        json_schema_extra={
            "description": "Целевая сумма проекта",
            "example": "1000",
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
        min_length=5,
        max_length=100,
        json_schema_extra={
            "description": "Название проекта",
            "example": "Помощь котикам",
        },
    )

    description: Optional[str] = Field(
        None,
        min_length=10,
        json_schema_extra={
            "description": "Описание проекта",
            "example": "На корм для котиков",
        },
    )

    full_amount: Optional[PositiveInt] = Field(
        None,
        json_schema_extra={
            "description": "Целевая сумма проекта",
            "example": "2000",
        },
    )

    class Config:
        extra = "forbid"
