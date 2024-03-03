from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.google_client import COLUMN_COUNT, FORMAT, ROW_COUNT

ERROR_MAX_ROW_COUNT = (
    'Количество строк {rows} больше максимального значения {max_rows}'
)
ERROR_MAX_COLUMN_COUNT = (
    'Количество колонок {columns} больше максимального значения {max_columns}'
)

HEADER = [
    ['Отчёт от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

SPREADSHEET_BODY = {
    'properties': {
        'title': 'Отчет на {date}',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': ROW_COUNT,
                'columnCount': COLUMN_COUNT
            }
        }
    }]
}


async def spreadsheets_create(
        wrapper_service: Aiogoogle,
        date: datetime = datetime.now().strftime(FORMAT)
) -> str:
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = spreadsheet_body[
        'properties'
    ][
        'title'
    ].format(date=date)
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(
            json=spreadsheet_body
        )
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        completed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    header = deepcopy(HEADER)
    header[0].append(datetime.now().strftime(FORMAT))
    table_values = [
        *header,
        *[
            list(
                map(
                    str,
                    [
                        project.name,
                        project.close_date - project.create_date,
                        project.description
                    ]
                )
            )
            for project in completed_projects
        ]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    column_count = max(len(column) for column in table_values)
    if len(table_values) > ROW_COUNT:
        raise ValueError(
            ERROR_MAX_ROW_COUNT.format(
                rows=len(table_values),
                max_rows=ROW_COUNT
            )
        )
    if column_count > COLUMN_COUNT:
        raise ValueError(
            ERROR_MAX_COLUMN_COUNT.format(
                columns=column_count,
                max_columns=COLUMN_COUNT
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{len(table_values)}C{column_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
