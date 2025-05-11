from fastapi import APIRouter, HTTPException
from typing import List
from models import TemaEvento
from database import get_connection


router = APIRouter()

#Devuelve todos los temas-eventos en una lista
@router.get("/temas-eventos", response_model=List[TemaEvento])
def get_temas_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tema_evento")
        temas_eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return temas_eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo tema-evento
@router.post("/tema-evento")
def create_tema_evento(tema_evento: TemaEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tema_evento (nombre) 
            VALUES (%s)
            """,
            (
                tema_evento.nombre,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tema-evento creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un tema-evento por su id
@router.get("/tema-evento/{tema_evento_id}", response_model=TemaEvento)
def get_tema_evento(tema_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tema_evento WHERE id = %s", (tema_evento_id,))
        tema_evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if tema_evento is None:
            raise HTTPException(status_code=404, detail="Tema-evento no encontrado")
        return tema_evento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Actualiza un tema-evento por su id
@router.put("/tema-evento/{tema_evento_id}")
def update_tema_evento(tema_evento_id: int, tema_evento: TemaEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tema_evento 
            SET nombre = %s
            WHERE id = %s
            """,
            (
                tema_evento.nombre,
                tema_evento_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tema-evento actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Elimina un tema-evento por su id
@router.delete("/tema-evento/{tema_evento_id}")
def delete_tema_evento(tema_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tema_evento WHERE id = %s", (tema_evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tema-evento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))