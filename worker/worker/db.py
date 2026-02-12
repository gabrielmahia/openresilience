import psycopg
from worker.settings import Settings

def conn():
    s=Settings()
    c=psycopg.connect(s.postgres_url)
    c.autocommit=True
    return c
