import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from middleware.routers.v1.main import api_router
from utils.config import settings
from layers.models.v1.core.db_handler import sessionmanager
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException
from middleware.authentication.authentication import TokenBasedAuthentication
from layers.models.v1.core.db_handler import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(TokenBasedAuthentication)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"message":str(exc.detail)}, status_code=exc.status_code)

@app.get("/")
async def root():
    return {"message": "Welcome to Reorganized API"}