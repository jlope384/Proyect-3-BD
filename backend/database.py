import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),  # Se usa la variable de entorno DB_HOST
        dbname=os.getenv("DB_NAME"),  # Se usa la variable de entorno DB_NAME
        user=os.getenv("DB_USER"),  # Se usa la variable de entorno DB_USER
        password=os.getenv("DB_PASSWORD"),  # Se usa la variable de entorno DB_PASSWORD
        port=os.getenv("DB_PORT"),  # Se usa la variable de entorno DB_PORT
        cursor_factory=RealDictCursor
    )