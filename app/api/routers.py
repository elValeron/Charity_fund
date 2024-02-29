from fastapi import APIRouter

from .enpoints.charity_project import charity_project_router
from .enpoints.donation import donation_router
from .enpoints.google_api import google_api_router
from .enpoints.user import router

main_router = APIRouter()

main_router.include_router(
    router=charity_project_router,
    prefix='/charity_project',
    tags=['Charity Project']
)
main_router.include_router(
    router=donation_router,
    prefix='/donation',
    tags=['Donation']
)
main_router.include_router(
    router=google_api_router,
    prefix='/google',
    tags=['Google']
)
main_router.include_router(router)
