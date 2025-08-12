from datetime import datetime
import requests
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(Path(__file__).parent)))
from utils.config import settings
from sqlalchemy import insert,create_engine, Table, MetaData
import datetime
import random
from layers.models.v1.core.system_models import Base

POSTGRES_URL: str = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_SERVER"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

def check_user_company(user, company):
    return user['company_name'] == company

def main():
    engine = create_engine(POSTGRES_URL)
    conn = engine.connect()
    Base.metadata.create_all(engine)
    metadata = MetaData()

    companiesTable = Table('companies', metadata, autoload_with=engine)
    usersTable = Table('users', metadata, autoload_with=engine)
    projectsTable = Table('projects', metadata, autoload_with=engine)
    projectsMembershipsTable = Table('projects_memberships', metadata, autoload_with=engine)

    request_session = requests.Session()

    try:
        url_wikipedia = settings.CHALLENGES_API_URL + f'/{settings.CANDIDATE_ID}/users'

        request_headers = {
            "X-API-Key": settings.CHALLENGES_API_KEY
        }

        request = request_session.get(url=url_wikipedia, headers=request_headers)
        request = request.json()
    except:
        return 0
    
    if "users" not in request:
        return 0

    users_request = request['users']
    companies = set()
    users_cleaned = []

    for user in users_request:
        if not isinstance(user, str):
            continue
        if "@" not in user:
            continue

        company_domain = user.split('@')[-1]
        company = company_domain.split('.')[0]
        companies.add(company)
        users_cleaned.append({
            "username": user.split('@')[0],
            "email": user,
            "company_name": company
        })

    for company_name in companies:
        stmt = insert(companiesTable).values(
            [{'name': company_name, 'created_at': datetime.datetime.now()}]
        ).returning(companiesTable.c.ID)

        with engine.begin() as conn:
            transaction_result = conn.execute(stmt)
            company_id = transaction_result.fetchone()

            if company_id is not None:
                company_id = company_id[0]
            else:
                continue
            
            users_of_this_company = list(filter(lambda user: check_user_company(user, company_name), users_cleaned))

            number_of_projects = random.randint(1,2)
            projects_ids = []
            users_ids = []

            for project in range(0, number_of_projects):
                stmt = insert(projectsTable).values(
                    [
                        {
                            'ID_company': company_id, 
                            'name': f'Project {project}',
                            'description': 'Custom description for this project',
                            'created_at': datetime.datetime.now(),
                        }
                    ]
                ).returning(projectsTable.c.ID)
                transaction_result = conn.execute(stmt)
                project_id = transaction_result.fetchone()

                if project_id is not None:
                    project_id = project_id[0]
                else:
                    continue

                projects_ids.append(project_id)
            
            for user in users_of_this_company:
                stmt = insert(usersTable).values(
                    [
                        {
                            'ID_company': company_id, 
                            'username': user['username'],
                            'email': user['email'],
                            'created_at': datetime.datetime.now(),
                        }
                    ]
                ).returning(usersTable.c.ID)
                transaction_result = conn.execute(stmt)
                user_id = transaction_result.fetchone()

                if user_id is not None:
                    user_id = user_id[0]
                else:
                    continue

                users_ids.append(user_id)

            index_for_project_management = len(users_ids)

            if(len(projects_ids) == 2):
                index_for_project_management = round(len(users_ids) / 2)

            for index, user_id in enumerate(users_ids):
                project_designated_for_this_user = \
                projects_ids[0] if index < index_for_project_management else projects_ids[1]

                stmt = insert(projectsMembershipsTable).values(
                    [
                        {
                            'ID_company': company_id, 
                            'ID_user': user_id,
                            'ID_project': project_designated_for_this_user,
                            'created_at': datetime.datetime.now(),
                        }
                    ]
                ).returning(projectsMembershipsTable.c.ID)
                conn.execute(stmt)

    return 1

if __name__ == "__main__":
    main()