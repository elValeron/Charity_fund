from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.api.validation import (
    check_charity_project_exists,
    check_name_duplicate,
    check_project_before_edit,
    check_project_before_remove
)
from app.services import invest

charity_project_router = APIRouter()


@charity_project_router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@charity_project_router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, None, session)
    new_project = await charity_project_crud.create(charity_project, session)
    session.add_all(
        invest(
            new_project,
            await donation_crud.get_opened_investments(
                session
            )
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@charity_project_router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, charity_project_id, session)
    valid_data = check_project_before_edit(charity_project, obj_in)
    charity_project = await charity_project_crud.update(
        valid_data, obj_in, session
    )
    return charity_project


@charity_project_router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_remove(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id,
        session
    )
    check_project_before_remove(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project
