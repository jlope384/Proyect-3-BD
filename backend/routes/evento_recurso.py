from fastapi import APIRouter, HTTPException
from typing import List
from models import EventoRecurso
from database import get_connection

router = APIRouter()

#Devuelve todos los eventos-recursos en una lista
@router.get("/eventos-recursos", response_model=List[EventoRecurso])
def get_eventos_recursos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_recurso")
        eventos_recursos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos_recursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo evento-recurso
@router.post("/evento-recurso")
def create_evento_recurso(evento_recurso: EventoRecurso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO evento_recurso (id_evento, id_recurso, cantidad) 
            VALUES (%s, %s, %s)
            """,
            (
                evento_recurso.id_evento,
                evento_recurso.id_recurso,
                evento_recurso.cantidad,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-recurso creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un evento-recurso por su id
@router.get("/evento-recurso/{evento_recurso_id}", response_model=EventoRecurso)
def get_evento_recurso(evento_recurso_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_recurso WHERE id = %s", (evento_recurso_id,))
        evento_recurso = cursor.fetchone()
        cursor.close()
        conn.close()
        if evento_recurso is None:
            raise HTTPException(status_code=404, detail="Evento-recurso no encontrado")
        return evento_recurso
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un evento-recurso por su id
@router.put("/evento-recurso/{evento_recurso_id}")
def update_evento_recurso(evento_recurso_id: int, evento_recurso: EventoRecurso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE evento_recurso SET id_evento = %s, id_recurso = %s, cantidad = %s WHERE id = %s",
            (evento_recurso.id_evento, evento_recurso.id_recurso, evento_recurso.cantidad, evento_recurso_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-recurso actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un evento-recurso por su id
@router.delete("/evento-recurso/{evento_recurso_id}")
def delete_evento_recurso(evento_recurso_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evento_recurso WHERE id = %s", (evento_recurso_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-recurso eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    