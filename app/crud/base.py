from typing import Optional, Sequence

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class BaseCRUD:
    """
    Базовые CRUD-методы
    """

    def __init__(self, model) -> None:
        self.model = model

    async def get(
        self,
        object_id: int,
        session: AsyncSession,
    ) -> Optional[object]:
        """
        Метод для получения объекта по id

        :param object_id: id записи
        :param session: сессия
        :return: запись из БД
        """
        object_id = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return object_id.scalars().first()

    async def get_all(
        self,
        session: AsyncSession,
        filters: Optional[list] = None,
        order_by: Optional[list] = None,
    ) -> Sequence:
        """
        Метод для получения всех объектов заданной модели

        :param session: сессия
        :param filters: список условий WHERE
        :param order_by: список полей сортировки
        :return: записи из БД
        """
        query = select(self.model)

        if filters:
            query = query.where(*filters)
        if order_by:
            query = query.order_by(*order_by)

        db_objects = await session.execute(query)
        return db_objects.scalars().all()

    async def create(
        self, input_obj, session: AsyncSession, user: Optional[User] = None
    ) -> object:
        """
        Метод для добавления записи в БД

        :param input_obj: входящий объект
        :param session: сессия
        :param user: id пользователя
        :return: созданный объект из БД
        """
        input_obj_data = input_obj.dict()

        if user is not None:
            input_obj_data["user_id"] = user.id

        db_obj = self.model(**input_obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        input_obj,
        session: AsyncSession,
    ) -> object:
        """
        Метод для обновления записи из БД

        :param db_obj: объект из БД
        :param input_obj: входящий объект
        :param session: сессия
        :return: обновленный объект из БД
        """
        input_obj_data = jsonable_encoder(db_obj)
        update_data = input_obj.dict(exclude_unset=True)

        for field in input_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj,
        session: AsyncSession,
    ) -> object:
        """
        Метод для удаления записи из БД

        :param db_obj: объект из БД
        :param session: сессия
        :return: удаленный объект из БД
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def save(self, db_obj, session: AsyncSession) -> object:
        """
        Метод для сохранения одной записи в БД.

        :param db_obj: объект из БД
        :param session: сессия
        :return: сохранённый объект из БД
        """
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def save_many(self, session: AsyncSession, *db_objs) -> None:
        """
        Метод для сохранения
        нескольких объектов в БД одним коммитом.

        :param session: сессия
        :param db_objs: объекты из БД
        :return: None, сохраняет данные в БД
        """
        for obj in db_objs:
            session.add(obj)
        await session.commit()
