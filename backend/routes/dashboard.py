from fastapi import APIRouter, HTTPException
from database import get_connection
import psycopg2
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

def verify_tables_exist(cursor):
    required_tables = [
        'evento', 'entrada', 'registro_asistencia', 
        'calificacion_evento', 'asistente'
    ]
    
    for table in required_tables:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table}'
            )
        """)
        if not cursor.fetchone()[0]:
            raise HTTPException(
                status_code=503,
                detail=f"La tabla {table} no existe en la base de datos"
            )

@router.get("/dashboard")
async def get_dashboard_stats():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar existencia de tablas
        verify_tables_exist(cursor)
        
        # Consulta 1: Total eventos
        cursor.execute("SELECT COUNT(*) FROM evento")
        total_eventos = cursor.fetchone()[0] or 0
        
        # Consulta 2: Total asistentes únicos
        cursor.execute("SELECT COUNT(DISTINCT id_asistente) FROM entrada")
        total_asistentes = cursor.fetchone()[0] or 0
        
        # Consulta 3: Promedio asistencia por evento
        cursor.execute("""
            SELECT COALESCE(AVG(subquery.asistentes), 0) 
            FROM (
                SELECT COUNT(id_asistente) as asistentes 
                FROM registro_asistencia 
                GROUP BY id_evento
            ) subquery
        """)
        promedio_asistencia = float(cursor.fetchone()[0] or 0)
        
        # Consulta 4: Calificación promedio
        cursor.execute("""
            SELECT COALESCE(AVG(calificacion), 0) 
            FROM calificacion_evento
            WHERE calificacion IS NOT NULL
        """)
        calificacion_promedio = float(cursor.fetchone()[0] or 0)
        
        # Consulta 5: Total recaudado
        cursor.execute("""
            SELECT COALESCE(SUM(precio_final), 0) 
            FROM entrada
            WHERE precio_final IS NOT NULL
        """)
        total_recaudado = float(cursor.fetchone()[0] or 0)

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "totalEventos": int(total_eventos),
                "totalAsistentes": int(total_asistentes),
                "promedioAsistencia": round(promedio_asistencia, 2),
                "calificacionPromedio": round(calificacion_promedio, 1),
                "totalRecaudado": round(total_recaudado, 2)
            }
        }
        
    except psycopg2.OperationalError as e:
        logger.error(f"Error de conexión a DB: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "message": "Error de conexión a la base de datos",
                "error": str(e)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Error interno del servidor",
                "error": str(e)
            }
        )
    finally:
        if conn:
            cursor.close()
            conn.close()