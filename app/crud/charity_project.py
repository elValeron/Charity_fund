from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        completed_projects = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.fully_invested
            ).order_by(
                extract(
                    'epoch', CharityProject.close_date
                ) - extract(
                    'epoch',
                    CharityProject.create_date
                )
            )
        )
        return completed_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
