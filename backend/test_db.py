# Crea un script test_db.py
import psycopg2
from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Conexión exitosa:", cursor.fetchone())
except Exception as e:
    print("Error de conexión:", e)
finally:
    if 'conn' in locals():
        conn.close()