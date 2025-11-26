from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_donations_in_projects(
    project: CharityProject, session: AsyncSession
) -> None:
    """
    Определяет распределение донатов и закрытие проекта.

    Алгоритм:
    1. Вычисляет оставшуюся сумму для закрытия проекта.
    2. Берет незакрытые пожертвования по порядку создания.
    3. Распределяет пожертвования до полной суммы проекта.
    4. Обновляет статусы пожертвований и проекта.
    5. Сохраняет изменения в БД.

    :param project: проект, в который будем инвестировать.
    :param session: сессия
    :return: None
    """
    # Вычисляет оставшуюся сумму
    remaining = project.full_amount - project.invested_amount

    # Берет незакрытые пожертвования
    donations = await donation_crud.get_all(
        session=session,
        filters=[Donation.fully_invested.is_(False)],
        order_by=[Donation.create_date],
    )

    # Проходит по каждому пожертвованию
    for donation in donations:

        if remaining <= 0:
            break  # Проект профинансирован, выходит

        # Вычисляет доступную для инвестирования сумму в пожертвовании
        donate_remaining = donation.full_amount - donation.invested_amount

        # Определяет сумму для инвестирования
        invest_amount = min(remaining, donate_remaining)

        # Обновляет суммы проинвестированных средств
        donation.invested_amount += invest_amount
        project.invested_amount += invest_amount
        remaining -= invest_amount

        # Если пожертвование полностью использовано, закрывает
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now(timezone.utc)

        # Сохраняет в БД
        await donation_crud.save(donation, session)
        await session.refresh(project)

    # Если проект полностью профинансирован, закрывает
    if project.invested_amount >= project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now(timezone.utc)

    # Сохраняет в БД
    await project_crud.save(project, session)
