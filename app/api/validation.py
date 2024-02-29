from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


DUBLICATE_NAME_ERROR = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найдена!'
CLOSED_PROEJECT_CANNOT_EDIT = 'Закрытый проект нельзя редактировать!'
INVESTED_AMOUNT_GREATED_FULL_INVESTED = (
    'Сумма инвестиций превышает полную стоимость проекта!'
)
INVESTED_PROJECT_CANNOT_REMOVE = (
    'В проект были внесены средства, не подлежит удалению!'
)


async def check_name_duplicate(
        project_name: str,
        current_project_id: int,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id and current_project_id != project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DUBLICATE_NAME_ERROR,
        )
    return project_name


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


def check_project_before_edit(
        project: CharityProject,
        update_data: CharityProjectUpdate
) -> CharityProject:
    update_data.full_amount = (
        project.full_amount if not update_data.full_amount
        else update_data.full_amount
    )
    if project.invested_amount > update_data.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_AMOUNT_GREATED_FULL_INVESTED
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_PROEJECT_CANNOT_EDIT
        )
    if project.invested_amount == update_data.full_amount:
        project.fully_invested = True
    return project


def check_project_before_remove(
        project: CharityProject,
) -> None:
    if project.invested_amount or project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_PROJECT_CANNOT_REMOVE
        )
