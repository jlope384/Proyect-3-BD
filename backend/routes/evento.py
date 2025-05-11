from fastapi import APIRouter, HTTPException
from typing import List
from models import Evento
from database import get_connection

router = APIRouter()

#Devuelve todos los eventos en una lista
@router.get("/eventos", response_model=List[Evento])
def get_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento")
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Crea un nuevo 
@router.post("/evento")
def create_evento(evento: Evento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO evento (nombre, fecha, hora, descripcion, id_lugar, id_categoria_evento, id_tipo_evento, id_tema_evento, id_usuario) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                evento.nombre,
                evento.fecha,
                evento.hora,
                evento.descripcion,
                evento.id_lugar,
                evento.id_categoria_evento,
                evento.id_tipo_evento,
                evento.id_tema_evento,
                evento.id_usuario,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un evento por su id
@router.get("/evento/{evento_id}", response_model=Evento)
def get_evento(evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento WHERE id = %s", (evento_id,))
        evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return evento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un evento por su id
@router.put("/evento/{evento_id}")
def update_evento(evento_id: int, evento: Evento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE evento 
            SET nombre = %s, fecha = %s, hora = %s, descripcion = %s, id_lugar = %s, id_categoria_evento = %s, id_tipo_evento = %s, id_tema_evento = %s, id_usuario = %s 
            WHERE id = %s
            """,
            (
                evento.nombre,
                evento.fecha,
                evento.hora,
                evento.descripcion,
                evento.id_lugar,
                evento.id_categoria_evento,
                evento.id_tipo_evento,
                evento.id_tema_evento,
                evento.id_usuario,
                evento_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un evento por su id
@router.delete("/evento/{evento_id}")
def delete_evento(evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evento WHERE id = %s", (evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
