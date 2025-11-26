from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.services.google_api import update_spreadsheets_value

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """
    Создание отчета в Google Sheets
    """
    # Получаем проекты из БД
    projects = await project_crud.get_projects_by_completion_rate(session)

    SPREADSHEET_ID = "1vbkAT4-PJhnyqSb7yahCUOinUNOKt8hFtAnTYGcv4xw"

    # Обновляем отчет в Google Sheets
    await update_spreadsheets_value(SPREADSHEET_ID, projects, wrapper_services)

    return projects
