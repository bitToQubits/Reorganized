from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.core.system_models import UsersTable, CompaniesTable
 
class UsersModel():
    async def get_statistics(self, db_session: AsyncSession):
        stmt = \
        select(func.count("*")) \
        .select_from(UsersTable)

        users_registered_query = await db_session.execute(stmt)
        users_registered_query = users_registered_query.fetchone()
        
        users_registered = -1

        if users_registered_query is not None:
            users_registered = users_registered_query[0]

        count_users_expression = func.count(UsersTable.ID).label("count_users")

        stmt = \
        select(
            CompaniesTable.ID,
            CompaniesTable.name, 
            count_users_expression
        ) \
        .select_from(CompaniesTable) \
        .join(UsersTable, CompaniesTable.ID == UsersTable.ID_company) \
        .group_by(CompaniesTable.ID) \
        .order_by(count_users_expression.desc()) \
        .limit(5)

        companies_users_count_not_processed = await db_session.execute(stmt)

        return {
            "companies_users_count_not_processed": companies_users_count_not_processed,
            "users_registered": users_registered
        }


users_model = UsersModel()
