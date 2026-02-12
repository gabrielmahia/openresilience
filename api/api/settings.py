import os
from pydantic import BaseModel
class Settings(BaseModel):
    postgres_url: str = os.environ['POSTGRES_URL']
    redis_url: str = os.environ['REDIS_URL']
    version: str = os.environ.get('OR_VERSION','0.3.0')
    rate_limit_per_minute: int = int(os.environ.get('RATE_LIMIT_PER_MINUTE','60'))
    reports_per_ip_per_hour: int = int(os.environ.get('REPORTS_PER_IP_PER_HOUR','30'))
    subs_per_ip_per_hour: int = int(os.environ.get('SUBS_PER_IP_PER_HOUR','30'))
