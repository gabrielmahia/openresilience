import os, psycopg

def conn():
    c=psycopg.connect(os.environ['POSTGRES_URL'])
    c.autocommit=True
    return c
