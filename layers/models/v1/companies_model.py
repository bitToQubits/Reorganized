from datetime import datetime
from sqlalchemy import select, insert
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from layers.models.v1.core.system_models import UsersTable, CompaniesTable

class CompaniesCreateDTO(BaseModel):
    name: str

class CompaniesModel():
    async def save_company(self, company_object: CompaniesCreateDTO, db_session: AsyncSession):
        stmt = insert(CompaniesTable).values(
            [
                {
                    'name': company_object.name, 
                    'created_at': datetime.datetime.now()
                }
            ]
        ).returning(CompaniesTable.ID)

        transaction_result = await db_session.execute(stmt)
        await db_session.commit()
        transaction_result = transaction_result.fetchone()

        if transaction_result is not None:
            company_id = transaction_result[0]
        else:
            company_id = 0

        return company_id
    
    async def get_companies(self, offset: int, db_session: AsyncSession):
        stmt = select(
            CompaniesTable.ID,
            CompaniesTable.name,
            CompaniesTable.created_at,
        ).offset(offset).limit(100).order_by(CompaniesTable.ID.desc())

        companies_list_not_processed = await db_session.execute(stmt)

        return companies_list_not_processed
    
    async def get_users_company(self, company_id:int, offset: int, db_session: AsyncSession):
        stmt = \
        select(
            UsersTable.ID, 
            UsersTable.email, 
            UsersTable.username
        ) \
        .select_from(UsersTable) \
        .where(UsersTable.ID_company == company_id)

        users_company_list_not_processed = await db_session.execute(stmt)

        return users_company_list_not_processed

companies_model = CompaniesModel()