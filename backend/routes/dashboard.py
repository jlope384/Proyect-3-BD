from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Total eventos
        cursor.execute("SELECT COUNT(*) FROM evento")
        total_eventos = cursor.fetchone()[0]
        
        # Total asistentes
        cursor.execute("SELECT COUNT(DISTINCT id_asistente) FROM entrada")
        total_asistentes = cursor.fetchone()[0]
        
        # Promedio asistencia
        cursor.execute("""
            SELECT AVG(asistentes) 
            FROM (
                SELECT COUNT(id_asistente) as asistentes 
                FROM registro_asistencia 
                GROUP BY id_evento
            ) subquery
        """)
        promedio_asistencia = cursor.fetchone()[0] or 0
        
        # Calificación promedio
        cursor.execute("SELECT AVG(calificacion) FROM calificacion_evento")
        calificacion_promedio = cursor.fetchone()[0] or 0
        
        # Total recaudado
        cursor.execute("SELECT SUM(precio_final) FROM entrada")
        total_recaudado = cursor.fetchone()[0] or 0
        
        return {
            "totalEventos": total_eventos,
            "totalAsistentes": total_asistentes,
            "promedioAsistencia": float(promedio_asistencia),
            "calificacionPromedio": float(calificacion_promedio),
            "totalRecaudado": float(total_recaudado)
        }
        
    except Exception as e:
        print("Error en dashboard:", str(e))
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()