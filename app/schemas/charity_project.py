from typing import Annotated, Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import DBInfo


class CharityProjectBase(BaseModel):
    """
    Базовая схема проекта
    """

    name: Annotated[
        str,
        Field(
            min_length=5,
            max_length=100,
            json_schema_extra={
                "description": "Название проекта",
                "example": "Помощь котикам",
            },
        ),
    ]

    description: Annotated[
        str,
        Field(
            min_length=10,
            json_schema_extra={
                "description": "Описание проекта",
                "example": "На корм для котиков",
            },
        ),
    ]

    full_amount: Annotated[
        PositiveInt,
        Field(
            json_schema_extra={
                "description": "Целевая сумма проекта",
                "example": "1000",
            },
        ),
    ]


class CharityProjectCreate(CharityProjectBase):
    """
    Схема запроса для создания проекта
    """

    model_config = {"extra": "forbid"}


class CharityProjectDB(DBInfo, CharityProjectBase):
    """
    Схема ответа, описывает возвращаемый из БД объект
    """


class CharityProjectUpdate(BaseModel):
    """
    Схема запроса для обновления
    """

    name: Annotated[
        Optional[str],
        Field(
            min_length=5,
            max_length=100,
            json_schema_extra={
                "description": "Название проекта",
                "example": "Помощь котикам",
            },
        ),
    ] = None

    description: Annotated[
        Optional[str],
        Field(
            min_length=10,
            json_schema_extra={
                "description": "Описание проекта",
                "example": "На корм для котиков",
            },
        ),
    ] = None

    full_amount: Annotated[
        Optional[PositiveInt],
        Field(
            json_schema_extra={
                "description": "Целевая сумма проекта",
                "example": "2000",
            },
        ),
    ] = None

    class Config:
        extra = "forbid"
