from fastapi import APIRouter
from layers.controllers.v1.users_controller import users_controller
from layers.dependencies.v1.core import DBSessionDep

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('/statistics')
async def get_statistics(db_session: DBSessionDep):
    return await users_controller.get_statistics(db_session)