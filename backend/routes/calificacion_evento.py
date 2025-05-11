from fastapi import APIRouter, HTTPException
from typing import List
from models import CalificacionEvento
from database import get_connection

router = APIRouter()

#Devuelve todas las calificaciones de eventos en una lista
@router.get("/calificaciones-eventos", response_model=List[CalificacionEvento])
def get_calificaciones_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calificacion_evento")
        calificaciones_eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return calificaciones_eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea una nueva calificacion de evento
@router.post("/calificacion-evento")
def create_calificacion_evento(calificacion_evento: CalificacionEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO calificacion_evento (id_evento, id_asistente, calificacion, comentario) 
            VALUES (%s, %s, %s)
            """,
            (
                calificacion_evento.id_evento,
                calificacion_evento.id_asistente,
                calificacion_evento.calificacion,
                calificacion_evento.comentario,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Calificacion de evento creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve una calificacion de evento por su id
@router.get("/calificacion-evento/{calificacion_evento_id}", response_model=CalificacionEvento)
def get_calificacion_evento(calificacion_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calificacion_evento WHERE id = %s", (calificacion_evento_id,))
        calificacion_evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if calificacion_evento is None:
            raise HTTPException(status_code=404, detail="Calificacion de evento no encontrada")
        return calificacion_evento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve todas las calificaciones de eventos por id_evento
@router.get("/calificaciones-eventos/evento/{id_evento}", response_model=List[CalificacionEvento])
def get_calificaciones_eventos_by_evento(id_evento: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calificacion_evento WHERE id_evento = %s", (id_evento,))
        calificaciones_eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        if not calificaciones_eventos:
            raise HTTPException(status_code=404, detail="No se encontraron calificaciones para este evento")
        return calificaciones_eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza una calificacion de evento por su id
@router.put("/calificacion-evento/{calificacion_evento_id}")
def update_calificacion_evento(calificacion_evento_id: int, calificacion_evento: CalificacionEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE calificacion_evento 
            SET id_evento = %s, id_asistente = %s, calificacion = %s, comentario = %s
            WHERE id = %s
            """,
            (
                calificacion_evento.id_evento,
                calificacion_evento.id_asistente,
                calificacion_evento.calificacion,
                calificacion_evento.comentario,
                calificacion_evento_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Calificacion de evento actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina una calificacion de evento por su id
@router.delete("/calificacion-evento/{calificacion_evento_id}")
def delete_calificacion_evento(calificacion_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calificacion_evento WHERE id = %s", (calificacion_evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Calificacion de evento eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))