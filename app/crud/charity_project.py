from datetime import datetime, timezone
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class ProjectCRUD(BaseCRUD):
    """
    CRUD-методы для проектов
    """

    async def get_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """
        Метод для проверки уникальности поля name.

        :param project_name: значение поля name
        :return: id записи из БД
        """
        db_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_id = db_id.scalars().first()
        return db_id

    async def update(
        self, db_obj, input_obj, session: AsyncSession
    ) -> Optional[int]:
        """
        Метод для обновления записи из БД.
        Дополненный с логикой закрытия проекта.

        :param db_obj: объект из БД
        :param input_obj: входящий объект
        :param session: сессия
        :return: обновленный объект из БД
        """
        # Стандартное обновление (как в BaseCRUD)
        input_obj_data = jsonable_encoder(db_obj)
        update_data = input_obj.dict(exclude_unset=True)

        for field in input_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # Дополнительная логика закрытия проекта
        if (
            db_obj.full_amount is not None
            and db_obj.invested_amount == db_obj.full_amount
            and not db_obj.fully_invested
        ):
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now(timezone.utc)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


project_crud = ProjectCRUD(CharityProject)
