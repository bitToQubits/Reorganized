import sys
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from layers.services.v1.companies_service import companies_service
from utils.response_messages import responses
from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.companies_model import CompaniesCreateDTO

class CompaniesController():
    async def save_company(self, company_object:CompaniesCreateDTO, db_session: AsyncSession):
        company_id = await companies_service.save_company(company_object, db_session)

        return JSONResponse(
            {
                'message': responses.success["COMPANY_SAVED"], 
                'company_id': company_id
            },
            status_code=200
        )
    
    async def get_companies(self, offset: int, db_session: AsyncSession):
        if offset < 0 or offset > sys.maxsize:
            raise HTTPException(status_code=422, detail=responses.error["OFFSET"])
        
        companies_list = await companies_service.get_companies(offset, db_session)
        
        return JSONResponse(
            {
                'message': responses.success["COMPANIES_LIST_RETRIEVED"], 
                'companies_list': companies_list
            },
            status_code=200
        )
    
    async def get_users_company(self, company_id:int, offset: int, db_session: AsyncSession):
        if offset < 0 or offset > sys.maxsize:
            raise HTTPException(status_code=422, detail=responses.error["OFFSET"])
        
        users_company_list = await companies_service.get_users_company(company_id, offset, db_session)

        return JSONResponse(
            {
                'message': responses.success["COMPANIES_USERS_LIST_RETRIEVED"], 
                'users_company_list': users_company_list
            },
            status_code=200
        )

companies_controller = CompaniesController()