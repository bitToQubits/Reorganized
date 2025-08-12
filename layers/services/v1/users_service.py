from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.users_model import users_model

class UsersService:
    async def get_statistics(self, db_session: AsyncSession):
        system_statistics = await users_model.get_statistics(db_session)

        companies_users_count = []
        for company_users_count in system_statistics["companies_users_count_not_processed"]:
            companies_users_count.append({
            "company_id": company_users_count[0],
            "company_name": company_users_count[1],
            "company_users_count": company_users_count[2]
        })

        return {
            "top_5_companies_with_more_users": companies_users_count,
            "users_registered_in_the_system": system_statistics["users_registered"]
        }
    
users_service = UsersService()