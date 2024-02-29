from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import invest
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBLong


donation_router = APIRouter()


@donation_router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donations: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        donations, session, user, skip_commit=True
    )
    session.add_all(
        invest(
            new_donation,
            await charity_project_crud.get_opened_investments(
                session
            )
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@donation_router.get(
    '/',
    response_model=list[DonationDBLong],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    get_all_donations = await donation_crud.get_multi(session)
    return get_all_donations


@donation_router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
