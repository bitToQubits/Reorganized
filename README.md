
# Reorganized - Project Management Platform API

Project management technical project made in FastAPI with SQLAlchemy + Alembic integrations. DB in PostgreSQL. 

## Setup instructions

Make sure you have installed on your project

- Python 3.10 or superior
- Docker Desktop (only if you want to setup by docker the DB, otherwise with Pgadmin & PostgreSQL installed would be ok)

Clone the repo in your directory of preference

Run this command on the root directory of the project to initialize a virtual environment.

(for windows users)

`` venv\Scripts\activate ``

(for mac os users)

`` source venv/bin/activate ``

Lets install the requirements and mandatory packages with this command

`` pip install -r requirements.txt ``

Finished the installation process, lets proceed to dockerize and initialize our db (this step is optional, if you have already installed postgresql in your sistem, only make sure to create a db for the system with the name of your preference)

Pull the lastest image of postgreSQL with this command in the terminal

`` docker pull postgres ``

Then, execute this command

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=[Your preferred password] \
  -e POSTGRES_USER=[Your preferred username] \
  -e POSTGRES_DB=[Your preferred db name]  \
  -p 5433:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

If you have conflicted ports (the -p 5433:5432 flag) just try different ports until the container starts.

Now, the final steps would be configuring the .env file.

This is a template of the .env file to be filled with your data.

```
CANDIDATE_ID=[Your candidate ID]
CHALLENGES_API_KEY=[Your API key for the Better Group Challenges API]
POSTGRES_USER=[Your postgre username]
POSTGRES_PASSWORD=[Your postgre password]
POSTGRES_SERVER=localhost
POSTGRES_PORT=[Your port, if you followed the docker procedure it must be 5433, otherwise it could be 5432]
POSTGRES_DB=[Your db name]
```

Now, lets create the schema (the tables) in our database. Run this command in the root directory.

`` alembic upgrade head ``

Finally, execute the API with this command (in the root directory of the project)

`` fastapi dev main.py ``

## Endpoints

To syncronize Reorganized with the Better Group API, execute the ``sincronization.py`` inside the scripts folder.

Base Path

```/api/v1```

Authentication

All endpoints require the HTTP header:

``` X-API-Key: y2p3B1Mb1T7dbZAOV5F1W2Eh5 ```

### Companies

#### Create a company
`POST` /companies/

Request body ``(JSON)``
```
{
  "name": "string"
}
```

Success response ``(200)``
```
{
  "message": "Company saved successfully",
  "company_id": 123
}
```

#### List companies
`GET` /companies/?offset={offset}

Query parameters
```
offset (optional, integer, default 0) -> pagination offset (limit 100 per page)
```

Success response ``(200)``
```
{
  "message": "Companies list successfully retrieved",
  "companies_list": [
    {
      "ID": 1,
      "company_name": "string",
      "creation_date": "YYYY-MM-DD HH:MM:SS"
    }
  ]
}
```

Error response ``(422)``

```
{
  "detail": "You must provide a valid offset for this query."
}
```

#### List users of a company
`GET` /companies/users?company_id={company_id}&offset={offset}

Query parameters

```
- company_id (required, integer) -> company identifier
- offset (optional, integer, default 0)
```

Success response ```(200)```

```
{
  "message": "Companies users list successfully retrieved",
  "users_company_list": [
    {
      "ID": 1,
      "email": "user@example.com",
      "username": "string"
    }
  ]
}
```

### Projects

#### Create a project
`POST` /projects/

Request body ```(JSON)```

```
{
  "company_id": integer,
  "name": "string",
  "description": "string"
}
```

Success response ``(201)``

```
{
  "message": "Project saved successfully",
  "project_id": 123
}
```

Error response ``(400)``

```
{
  "detail": "The IDs must be valid for the reorganized database"
}
```

#### List projects
`GET` /projects/?offset={offset}

```
Query parameters
- offset (optional, integer, default 0)
```

Success response ``(200)``

```
{
  "message": "Projects successfully retrieved",
  "projects_list": [
    {
      "ID": 1,
      "project_name": "string",
      "creation_date": "YYYY-MM-DD HH:MM:SS"
    }
  ]
}
```

Error response ``(422)``

```
{
  "detail": "You must provide a valid offset for this query."
}
```

#### Get project details
`GET` /projects/{project_id}

Path parameters

```
project_id (required, integer)
```

Success response ``(200)``

```
{
  "message": "Project details successfully retrieved",
  "project_details": {
    "ID": 1,
    "project_name": "string",
    "project_description": "string",
    "creation_date": "YYYY-MM-DD HH:MM:SS"
  }
}
```

#### Add user to project
`POST` /projects/membership

Request body (JSON)
{
  "company_id": 1,
  "project_id": 2,
  "user_id": 3
}

Success response (201)
{
  "message": "User successfully added to project",
  "project_membership_id": 456
}

Error responses

``406``
  {
    "detail": "This user is already in the specified project"
  }

``400``

```
  {
    "detail": "The IDs must be valid for the reorganized database"
  }
```

#### Remove user from project
`DELETE` /projects/membership

```
Request body (JSON)
{
  "company_id": 1,
  "project_id": 2,
  "user_id": 3
}
```

Success response ``(200)``

```
{
  "message": "User successfully removed from project"
}
```

Error response ``(406)``

```
{
  "detail": "This user is not in the specified project"
}
```

#### Project statistics
`GET` /projects/statistics

Success response ``(200)``

```
{
  "message": "Systems statistics successfully retrieved",
  "system_statistics": {
    "top_5_projects_with_less_users": [
      {
        "project_id": integer,
        "project_name": "string",
        "project_users_count": integer
      }
    ],
    "projects_created_in_the_system": integer
  }
}
```

### Users

#### Users statistics
`GET` /users/statistics

Success response ``(200)``

```
{
  "message": "Systems statistics successfully retrieved",
  "system_statistics": {
    "top_5_companies_with_more_users": [
      {
        "company_id": integer,
        "company_name": "string",
        "company_users_count": integer
      }
    ],
    "users_registered_in_the_system": integer
  }
}
```

# Jorge Luis Baez