from fastapi import APIRouter, HTTPException
from typing import List
from models import TipoEvento
from database import get_connection

router = APIRouter()

#Devuelve todos los tipos de eventos en una lista
@router.get("/tipos-eventos", response_model=List[TipoEvento])
def get_tipos_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_evento")
        tipos_eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return tipos_eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo tipo de evento
@router.post("/tipo-evento")
def create_tipo_evento(tipo_evento: TipoEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tipo_evento (nombre) 
            VALUES (%s)
            """,
            (
                tipo_evento.nombre,
                tipo_evento.descripcion,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de evento creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un tipo de evento por su id
@router.get("/tipo-evento/{tipo_evento_id}", response_model=TipoEvento)
def get_tipo_evento(tipo_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_evento WHERE id = %s", (tipo_evento_id,))
        tipo_evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if tipo_evento is None:
            raise HTTPException(status_code=404, detail="Tipo de evento no encontrado")
        return tipo_evento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un tipo de evento por su id
@router.put("/tipo-evento/{tipo_evento_id}")
def update_tipo_evento(tipo_evento_id: int, tipo_evento: TipoEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tipo_evento 
            SET nombre = %s, descripcion = %s
            WHERE id = %s
            """,
            (
                tipo_evento.nombre,
                tipo_evento.descripcion,
                tipo_evento_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de evento actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un tipo de evento por su id
@router.delete("/tipo-evento/{tipo_evento_id}")
def delete_tipo_evento(tipo_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo_evento WHERE id = %s", (tipo_evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de evento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    