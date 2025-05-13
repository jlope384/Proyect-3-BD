import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="eventos_db",
        user="postgres",
        password="",  
        port="5432"
    )