from fastapi import APIRouter
from layers.controllers.v1.companies_controller import companies_controller
from layers.dependencies.v1.core import DBSessionDep
from layers.models.v1.companies_model import CompaniesCreateDTO

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)

@router.post('/')
async def save_company(company_object: CompaniesCreateDTO, db_session: DBSessionDep):
    return await companies_controller.save_company(company_object, db_session)

@router.get('/')
async def get_companies(db_session: DBSessionDep, offset: int | None = None):
    if offset is None:
        offset = 0
    return await companies_controller.get_companies(offset, db_session)

@router.get('/users')
async def get_users_company(db_session: DBSessionDep, company_id:int, offset: int | None = None):
    if offset is None:
        offset = 0
    return await companies_controller.get_users_company(company_id, offset, db_session)