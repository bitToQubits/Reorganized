from sqlalchemy.ext.asyncio import AsyncSession
from layers.models.v1.projects_model import projects_model
from layers.models.v1.projects_model import ProjectsCreateDTO,ProjectsMembershipDTO

class ProjectsService:
    async def save_project(self, project_object: ProjectsCreateDTO, db_session: AsyncSession):
        return await projects_model.save_project(project_object, db_session)
    
    async def get_projects(self, offset:int, db_session: AsyncSession):
        projects_list_not_processed = await projects_model.get_projects(offset, db_session)

        projects_list = []
        for project in projects_list_not_processed:
            projects_list.append({
                "ID": project[0],
                "project_name": project[1],
                "creation_date": project[2].strftime("%Y-%m-%d %H:%M:%S"),
            })

        return projects_list
    
    async def get_project_details(self, project_id:int, db_session: AsyncSession):
        project_details = await projects_model.get_project_details(project_id, db_session)
        return project_details
    
    async def add_user_to_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        project_membership_id = await projects_model.add_user_to_project(membership_object, db_session)
        return project_membership_id
    
    async def remove_user_from_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        project_membership_status = await projects_model.remove_user_from_project(membership_object, db_session)
        return project_membership_status
    
    async def get_statistics(self, db_session: AsyncSession):
        system_statistics = await projects_model.get_statistics(db_session)

        projects_users_count_list = []
        for project_users_count in system_statistics["projects_users_count_not_processed"]:
            projects_users_count_list.append({
                "project_id": project_users_count[0],
                "project_name": project_users_count[1],
                "project_users_count": project_users_count[2]
            })

        return {
            "top_5_projects_with_less_users": projects_users_count_list,
            "projects_created_in_the_system": system_statistics["projects_created_in_the_system"]
        }

projects_service = ProjectsService()