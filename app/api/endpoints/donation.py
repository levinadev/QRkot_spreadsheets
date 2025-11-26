from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationCreateResponse,
    DonationDB,
    DonationUserResponse,
)
from app.services.investment import invest_donations_in_projects

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep,
) -> list[DonationDB]:
    """
    Просмотреть список всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_all(session)


@router.get(
    "/my",
    response_model=list[DonationUserResponse],
    response_model_exclude={"user_id"},
)
async def get_user_donations(
    session: SessionDep, user: Annotated[User, Depends(current_user)]
) -> list[DonationUserResponse]:
    """
    Просмотреть список пожертвований пользователя,
    выполняющего запрос.

    Только для зарегистрированных пользователей.
    """
    return await donation_crud.get_by_user(session=session, user=user)


@router.post(
    "/",
    response_model=DonationCreateResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
) -> DonationCreateResponse:
    """
    Создать пожертвование и привязать к пользователю.
    """
    # Создаём запись в БД
    new_db_entry = await donation_crud.create(donation, session, user)

    # Получаем все открытые проекты
    projects = await project_crud.get_all(session)
    session.expunge_all()

    # Распределяем новый донат по проектам
    for project in projects:
        await invest_donations_in_projects(project, session)

    return new_db_entry
