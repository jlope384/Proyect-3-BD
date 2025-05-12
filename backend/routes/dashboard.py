# backend/routes/dashboard.py
from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

@router.get("/", summary="Estadísticas generales del dashboard")
def get_dashboard_stats():
    """
    Devuelve estadísticas agregadas:
      - totalEventos
      - totalAsistentes
      - promedioAsistencia
      - calificacionPromedio
      - totalRecaudado
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1) Total de eventos
        cursor.execute("SELECT COUNT(*) AS total_eventos FROM evento;")
        row = cursor.fetchone()
        total_eventos = int(row["total_eventos"] or 0)

        # 2) Total de asistentes únicos
        cursor.execute("SELECT COUNT(DISTINCT id_asistente) AS total_asistentes FROM entrada;")
        row = cursor.fetchone()
        total_asistentes = int(row["total_asistentes"] or 0)

        # 3) Promedio de asistencia por evento
        cursor.execute("""
            SELECT COALESCE(AVG(cnt), 0) AS promedio_asistencia
            FROM (
                SELECT COUNT(id_asistente) AS cnt
                FROM registro_asistencia
                GROUP BY id_evento
            ) sub;
        """)
        row = cursor.fetchone()
        promedio_asistencia = float(row["promedio_asistencia"] or 0.0)

        # 4) Calificación promedio de eventos
        cursor.execute("SELECT COALESCE(AVG(calificacion), 0) AS calificacion_promedio FROM calificacion_evento;")
        row = cursor.fetchone()
        calificacion_promedio = float(row["calificacion_promedio"] or 0.0)

        # 5) Total recaudado por venta de entradas
        cursor.execute("SELECT COALESCE(SUM(precio_final), 0) AS total_recaudado FROM entrada;")
        row = cursor.fetchone()
        total_recaudado = float(row["total_recaudado"] or 0.0)

        return {
            "totalEventos": total_eventos,
            "totalAsistentes": total_asistentes,
            "promedioAsistencia": promedio_asistencia,
            "calificacionPromedio": calificacion_promedio,
            "totalRecaudado": total_recaudado,
        }
    except Exception as e:
        # Si algo falla, devolvemos el error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()
