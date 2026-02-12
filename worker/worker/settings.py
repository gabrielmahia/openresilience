import os
from pydantic import BaseModel
class Settings(BaseModel):
    postgres_url: str = os.environ['POSTGRES_URL']
    redis_url: str = os.environ['REDIS_URL']
    version: str = os.environ.get('OR_VERSION','0.3.0')
    grid_step_deg: float = float(os.environ.get('GRID_STEP_DEG','0.25'))
    adapter: str = os.environ.get('DATA_ADAPTER','synthetic')
