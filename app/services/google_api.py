from datetime import datetime

from aiogoogle import Aiogoogle

FORMAT = "%Y/%m/%d %H:%M:%S"


async def update_spreadsheets_value(
    spreadsheetid: str, projects: list, wrapper_services: Aiogoogle
) -> None:
    """
    Обновляет таблицу Google Sheets.

    :param spreadsheetid: ID таблицы
    :param projects: список проектов
    :param wrapper_services: объект Aiogoogle
    :return: None
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")

    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]

    for proj in projects:
        new_row = [proj["name"], f'{proj["days"]} дней', proj["description"]]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:E30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
