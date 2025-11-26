from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import BaseCRUD
from app.models import Donation, User


class DonationCRUD(BaseCRUD):
    """
    CRUD-методы для пожертвований
    """

    async def get_by_user(self, session: AsyncSession, user: User) -> Sequence:
        """
        Метод возвращает список всех донатов,
        связанных с пользователем, отправившим запрос.

        :param session: сессия
        :param user: id пользователя
        :return: записи из БД
        """
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
