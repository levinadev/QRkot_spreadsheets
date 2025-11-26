from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_id_exists,
    check_closed_project,
    check_full_amount_not_less_than_invested,
    check_name_duplicate,
    check_project_has_no_investments,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_donations_in_projects

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: SessionDep,
) -> list[CharityProjectDB]:
    """
    Просмотреть список всех целевых проектов
    """
    return await project_crud.get_all(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Создать целевой проект.
    Только для суперюзеров.
    """
    await check_name_duplicate(charity_project.name, session)
    new_db_entry = await project_crud.create(charity_project, session)

    # Пересчет донатов в проекты
    await invest_donations_in_projects(new_db_entry, session)

    return new_db_entry


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Редактировать целевой проект.
    Только для суперюзеров.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    # Ищем запись в БД по id
    db_record = await check_charity_project_id_exists(project_id, session)

    # Закрытый проект нельзя редактировать
    await check_closed_project(db_record)

    # Сумма не может быть меньше уже вложенной
    await check_full_amount_not_less_than_invested(
        obj_in.full_amount, db_record
    )

    # Проверка уникальности имени
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    # Обновляем запись и возвращаем клиенту
    return await project_crud.update(db_record, obj_in, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Удалить целевой проект.
    Только для суперюзеров.

    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    db_record = await check_charity_project_id_exists(project_id, session)

    # Запрещаем удаление проекта, в который уже вложены деньги
    await check_project_has_no_investments(db_record)

    # Удаляем запись и возвращаем клиенту
    return await project_crud.delete(db_record, session)
