from fastapi.responses import JSONResponse
from layers.services.v1.users_service import users_service
from sqlalchemy.ext.asyncio import AsyncSession
from utils.response_messages import responses

class UsersController():
    async def get_statistics(self, db_session: AsyncSession):
        system_statistics = await users_service.get_statistics(db_session)
        return JSONResponse(
            {
                'message': responses.success["STATISTICS_RETRIEVED"],
                'system_statistics': system_statistics
            },
            status_code=200
        )

users_controller = UsersController()