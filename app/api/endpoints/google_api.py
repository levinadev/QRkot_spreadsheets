from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import project_crud

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
)
async def get_report(session: AsyncSession = Depends(get_async_session)):
    """
    Создание отчета в Google Sheets
    """
    # Получаем проекты из БД
    projects = await project_crud.get_projects_by_completion_rate(session)
    return projects
