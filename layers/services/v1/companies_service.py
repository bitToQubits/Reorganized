from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.companies_model import companies_model
from layers.models.v1.companies_model import CompaniesCreateDTO

class CompaniesService:
    async def save_company(self, company_object: CompaniesCreateDTO, db_session: AsyncSession):
        return await companies_model.save_company(company_object, db_session)
    
    async def get_companies(self, offset:int, db_session: AsyncSession):
        companies_list_not_processed = await companies_model.get_companies(offset, db_session)

        companies_list = []
        for company in companies_list_not_processed:
            companies_list.append({
                "ID": company[0],
                "company_name": company[1],
                "creation_date": company[2].strftime("%Y-%m-%d %H:%M:%S"),
            })

        return companies_list
    
    async def get_users_company(self, company_id:int, offset:int, db_session: AsyncSession):
        users_company_list_not_processed = \
        await companies_model.get_users_company(company_id, offset, db_session)

        users_company_list = []
        for user in users_company_list_not_processed:
            users_company_list.append({
                "ID": user[0],
                "email": user[1],
                "username": user[2],
            })

        return users_company_list

companies_service = CompaniesService()