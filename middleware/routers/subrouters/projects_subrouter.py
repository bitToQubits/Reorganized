from fastapi import APIRouter
from layers.controllers.v1.projects_controller import projects_controller
from layers.dependencies.v1.core import DBSessionDep
from layers.models.v1.projects_model import ProjectsCreateDTO,ProjectsMembershipDTO

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.post('/')
async def save_project(project_object: ProjectsCreateDTO, db_session: DBSessionDep):
    return await projects_controller.save_project(project_object, db_session)

@router.get('/')
async def get_projects(db_session: DBSessionDep, offset: int | None = None):
    if offset is None:
        offset = 0
    return await projects_controller.get_projects(offset, db_session)

@router.get('/statistics')
async def get_statistics(db_session: DBSessionDep):
    return await projects_controller.get_statistics(db_session)

@router.get('/{project_id}')
async def get_project_details(project_id:int, db_session: DBSessionDep):
    return await projects_controller.get_project_details(project_id, db_session)

@router.post('/membership')
async def add_user_to_project(membership_object: ProjectsMembershipDTO, db_session: DBSessionDep):
    return await projects_controller.add_user_to_project(membership_object, db_session)

@router.delete('/membership')
async def remove_user_from_project(membership_object: ProjectsMembershipDTO, db_session: DBSessionDep):
    return await projects_controller.remove_user_from_project(membership_object, db_session)