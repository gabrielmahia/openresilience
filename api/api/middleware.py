from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from api.redis_client import rconn
from or_shared.rate_limit import token_bucket_allow
from api.settings import Settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        s = Settings()
        r = rconn()
        ip = request.client.host if request.client else "unknown"
        key = f"rl:ip:{ip}"
        cap = s.rate_limit_per_minute
        refill = cap / 60.0
        if not token_bucket_allow(r, key, capacity=cap, refill_per_sec=refill):
            return Response("Too Many Requests", status_code=429)
        return await call_next(request)
