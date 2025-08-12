from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func, select, insert, delete
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from layers.models.v1.core.system_models import ProjectsTable, ProjectsMembershipsTable, UsersTable
from utils.response_messages import responses

class ProjectsCreateDTO(BaseModel):
    company_id: int
    name: str
    description: str

class ProjectsMembershipDTO(BaseModel):
    company_id: int
    project_id: int
    user_id: int

class ProjectsModel():
    async def save_project(self, project_object: ProjectsCreateDTO, db_session: AsyncSession):
        stmt = insert(ProjectsTable).values(
            [
                {
                    'ID_company': project_object.company_id,
                    'name': project_object.name, 
                    'description': project_object.description, 
                    'created_at': datetime.datetime.now()
                }
            ]
        ).returning(ProjectsTable.ID)

        transaction_result = await db_session.execute(stmt)
        await db_session.commit()
        transaction_result = transaction_result.fetchone()

        if transaction_result is not None:
            project_id = transaction_result[0]
        else:
            project_id = 0

        return project_id
    
    async def get_projects(self, offset: int, db_session: AsyncSession):
        stmt = select(
            ProjectsTable.ID,
            ProjectsTable.name,
            ProjectsTable.created_at,
        ).offset(offset).limit(100).order_by(ProjectsTable.ID.desc())

        projects_list_not_processed = await db_session.execute(stmt)

        return projects_list_not_processed
    
    async def get_project_details(self, project_id:int, db_session: AsyncSession):
        stmt = \
        select(
            ProjectsTable.ID,
            ProjectsTable.name,
            ProjectsTable.description,
            ProjectsTable.created_at,
        ) \
        .select_from(ProjectsTable) \
        .where(ProjectsTable.ID == project_id)

        project_query_result = await db_session.execute(stmt)
        project_found = {}

        for project in project_query_result:
            project_found["ID"] = project[0]
            project_found["project_name"] = project[1]
            project_found["project_description"] = project[2]
            project_found["creation_date"] = project[3].strftime("%Y-%m-%d %H:%M:%S")

        if not project_found:
            raise HTTPException(detail=responses.error["PROJECT_NOT_FOUND"], status_code=404)

        return project_found
    
    async def add_user_to_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        stmt = \
        select(
            ProjectsMembershipsTable.ID,
        ) \
        .select_from(ProjectsMembershipsTable) \
        .where(ProjectsMembershipsTable.ID_project == membership_object.project_id) \
        .where(ProjectsMembershipsTable.ID_user == membership_object.user_id) \
        .where(ProjectsMembershipsTable.ID_company == membership_object.company_id)

        project_membership_query_result = await db_session.execute(stmt)
        project_membership_query_result = project_membership_query_result.fetchone()

        if project_membership_query_result is not None:
            raise HTTPException(detail=responses.error["USER_IS_ALREADY_IN_PROJECT"], status_code=406)
        
        stmt = insert(ProjectsMembershipsTable).values(
            [
                {
                    'ID_company': membership_object.company_id,
                    'ID_user': membership_object.user_id, 
                    'ID_project': membership_object.project_id,
                    'created_at': datetime.datetime.now()
                }
            ]
        ).returning(ProjectsMembershipsTable.ID)

        transaction_result = await db_session.execute(stmt)
        await db_session.commit()
        transaction_result = transaction_result.fetchone()

        if transaction_result is not None:
            project_membership_id = transaction_result[0]
        else:
            project_membership_id = 0

        return project_membership_id

    async def remove_user_from_project(self, membership_object: ProjectsMembershipDTO, db_session:AsyncSession):
        stmt = \
        select(
            ProjectsMembershipsTable.ID,
        ) \
        .select_from(ProjectsMembershipsTable) \
        .where(ProjectsMembershipsTable.ID_project == membership_object.project_id) \
        .where(ProjectsMembershipsTable.ID_user == membership_object.user_id) \
        .where(ProjectsMembershipsTable.ID_company == membership_object.company_id)

        project_membership_query_result = await db_session.execute(stmt)
        project_membership_query_result = project_membership_query_result.fetchone()

        if project_membership_query_result is None:
            raise HTTPException(detail=responses.error["USER_IS_NOT_IN_PROJECT"], status_code=406)
        
        stmt = delete(ProjectsMembershipsTable) \
        .where(ProjectsMembershipsTable.ID_project == membership_object.project_id) \
        .where(ProjectsMembershipsTable.ID_user == membership_object.user_id) \
        .where(ProjectsMembershipsTable.ID_company == membership_object.company_id) \

        await db_session.execute(stmt)
        await db_session.commit()

    async def get_statistics(self, db_session: AsyncSession):
        stmt = \
        select(func.count("*")) \
        .select_from(ProjectsTable)

        projects_created_query = await db_session.execute(stmt)
        projects_created_query = projects_created_query.fetchone()
        
        projects_created = -1

        if projects_created_query is not None:
            projects_created = projects_created_query[0]

        count_users_expression = func.count(ProjectsMembershipsTable.ID_user).label("count_users")

        stmt = \
        select(
            ProjectsTable.ID,
            ProjectsTable.name, 
            count_users_expression
        ) \
        .select_from(ProjectsTable) \
        .join(ProjectsMembershipsTable, ProjectsTable.ID == ProjectsMembershipsTable.ID_project) \
        .group_by(ProjectsTable.ID) \
        .order_by(count_users_expression.asc()) \
        .limit(5)

        projects_users_count_not_processed = await db_session.execute(stmt)

        return {
            "projects_users_count_not_processed": projects_users_count_not_processed,
            "projects_created_in_the_system": projects_created
        }
    

projects_model = ProjectsModel()