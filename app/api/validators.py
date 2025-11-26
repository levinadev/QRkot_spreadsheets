from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    input_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверяет уникальность поля name

    :param input_name: полученное name
    :param session: сессия
    :return: id из БД
    """
    db_id = await project_crud.get_by_name(input_name, session)
    if db_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_id_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Получение объекта по id

    :param charity_project_id: полученный id
    :param session: сессия
    :return: объект из БД
    """
    db_object = await project_crud.get(charity_project_id, session)
    if db_object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден!"
        )
    return db_object


async def check_project_has_no_investments(
    project: CharityProject,
) -> None:
    """
    Проверяет, что у проекта нет вложенных средств

    :param project: полученный проект из БД
    :return: None
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя удалить проект, в который уже внесены средства.",
        )


async def check_closed_project(
    project: CharityProject,
) -> None:
    """
    Проверяет, что проект ещё не закрыт

    :param project: полученный проект из БД
    :return: None
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя редактировать полностью проинвестированный проект.",
        )


async def check_full_amount_not_less_than_invested(
    new_full_amount: Optional[int],
    project: CharityProject,
) -> None:
    """
    Проверяет изменение full_amount

    :param new_full_amount: полученный full_amount
    :param project: полученный проект из БД
    :return: None
    """
    if (
        new_full_amount is not None and
        new_full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f"Нельзя установить требуемую сумму меньше уже вложенной "
                f"({project.invested_amount})."
            ),
        )
