from fastapi import APIRouter
from middleware.routers.v1.subrouters import companies_subrouter, users_subrouter, projects_subrouter

api_router = APIRouter()
api_router.include_router(companies_subrouter.router)
api_router.include_router(projects_subrouter.router)
api_router.include_router(users_subrouter.router)