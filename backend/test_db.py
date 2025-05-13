from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print("¡Conexión exitosa! Versión de PostgreSQL:", cursor.fetchone()[0])
except Exception as e:
    print("Error de conexión:", e)
finally:
    if 'conn' in locals():
        conn.close()