from fastapi import APIRouter, HTTPException
from typing import List
from models import EventoPatrocinador
from database import get_connection

router = APIRouter()

#Devuelve todos los eventos-patrocinadores en una lista
@router.get("/eventos-patrocinadores", response_model=List[EventoPatrocinador])
def get_eventos_patrocinadores():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_patrocinador")
        eventos_patrocinadores = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos_patrocinadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo evento-patrocinador
@router.post("/evento-patrocinador")
def create_evento_patrocinador(evento_patrocinador: EventoPatrocinador):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO evento_patrocinador (id_evento, id_patrocinador) 
            VALUES (%s, %s)
            """,
            (
                evento_patrocinador.id_evento,
                evento_patrocinador.id_patrocinador,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-patrocinador creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un evento-patrocinador por su id
@router.get("/evento-patrocinador/{evento_patrocinador_id}", response_model=EventoPatrocinador)
def get_evento_patrocinador(evento_patrocinador_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_patrocinador WHERE id = %s", (evento_patrocinador_id,))
        evento_patrocinador = cursor.fetchone()
        cursor.close()
        conn.close()
        if evento_patrocinador is None:
            raise HTTPException(status_code=404, detail="Evento-patrocinador no encontrado")
        return evento_patrocinador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un evento-patrocinador por su id
@router.put("/evento-patrocinador/{evento_patrocinador_id}")
def update_evento_patrocinador(evento_patrocinador_id: int, evento_patrocinador: EventoPatrocinador):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE evento_patrocinador 
            SET id_evento = %s, id_patrocinador = %s 
            WHERE id = %s
            """,
            (
                evento_patrocinador.id_evento,
                evento_patrocinador.id_patrocinador,
                evento_patrocinador_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-patrocinador actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#Elimina un evento-patrocinador por su id
@router.delete("/evento-patrocinador/{evento_patrocinador_id}")
def delete_evento_patrocinador(evento_patrocinador_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evento_patrocinador WHERE id = %s", (evento_patrocinador_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-patrocinador eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    