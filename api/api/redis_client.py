import redis
from api.settings import Settings

def rconn():
    s=Settings()
    return redis.Redis.from_url(s.redis_url, decode_responses=True)
