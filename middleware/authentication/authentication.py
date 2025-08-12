from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.config import settings

class TokenBasedAuthentication(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key_authentication = request.headers.get('X-API-Key')
        
        if(api_key_authentication != settings.API_KEY_AUTHENTICATION):
            return JSONResponse(content={'message': "Not authorized"}, status_code=401)
        
        response = await call_next(request)
        
        return response