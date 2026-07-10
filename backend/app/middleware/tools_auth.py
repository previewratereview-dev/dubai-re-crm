from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import get_settings

settings = get_settings()

TOOLS_PREFIX = "/api/tools"


class ToolsAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(TOOLS_PREFIX):
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key != settings.ELEVENLABS_TOOLS_API_KEY:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing API key"
                )
        return await call_next(request)
