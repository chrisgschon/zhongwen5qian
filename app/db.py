# postgres connector

import psycopg2
import pandas as pd
from sqlalchemy import create_engine 
import os

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_HOST = os.environ['POSTGRES_HOST']

class Db():
    def __init__(self, db="zhongwen", user="pg"):
        # self.conn = psycopg2.connect(database=db, user=user)
        # self.cur = self.conn.cursor()
        self.enginestr = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

    def create_engine(self):
        return create_engine(self.enginestr)


    

