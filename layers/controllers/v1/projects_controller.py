import sys
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from layers.services.v1.projects_service import projects_service
from utils.response_messages import responses
from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.projects_model import ProjectsCreateDTO,ProjectsMembershipDTO
from sqlalchemy.exc import IntegrityError

class ProjectsController():
    async def save_project(self, project_object:ProjectsCreateDTO, db_session: AsyncSession):
        try:
            project_id = await projects_service.save_project(project_object, db_session)
        except IntegrityError:
            raise HTTPException(
                detail = responses.error["ID_INTEGRITY"],
                status_code=400
            )

        return JSONResponse(
            {
                'message': responses.success["PROJECT_SAVED"], 
                'project_id': project_id
            }, 
            status_code=201
        )
    
    async def get_projects(self, offset: int, db_session: AsyncSession):
        if offset < 0 or offset > sys.maxsize:
            raise HTTPException(status_code=422, detail=responses.error["OFFSET"])
        
        projects_list = await projects_service.get_projects(offset, db_session)

        return JSONResponse(
            {
                'message': responses.success["PROJECTS_RETRIEVED"],
                'projects_list': projects_list
            }, 
            status_code=200
        )
    
    async def get_project_details(self, project_id:int, db_session: AsyncSession):
        project_details = await projects_service.get_project_details(project_id, db_session)
        return JSONResponse(
            {
                'message': responses.success["PROJECT_DETAILS_RETRIEVED"],
                'project_details': project_details
            }, 
            status_code=200
        )
    
    async def add_user_to_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        try:
            project_membership_id = await projects_service.add_user_to_project(membership_object, db_session)
        except IntegrityError:
            raise HTTPException(
                detail = responses.error["ID_INTEGRITY"],
                status_code=400
            )
        
        return JSONResponse(
            {
                'message': responses.success["MEMBERSHIP_ADDED"], 
                'project_membership_id': project_membership_id
            }, 
            status_code=201
        )
    
    async def remove_user_from_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        await projects_service.remove_user_from_project(membership_object, db_session)
        return JSONResponse(
            {
                'message': responses.success["MEMBERSHIP_REMOVED"], 
            }, 
            status_code=200
        )
    
    async def get_statistics(self, db_session: AsyncSession):
        system_statistics = await projects_service.get_statistics(db_session)
        return JSONResponse(
            {
                'message': responses.success["STATISTICS_RETRIEVED"],
                'system_statistics': system_statistics
            },
            status_code=200
        )

projects_controller = ProjectsController()