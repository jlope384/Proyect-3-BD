from fastapi import APIRouter, HTTPException
from typing import List
from models import EventoArtista
from database import get_connection

router = APIRouter()

#Devuelve todos los eventos-artistas en una lista
@router.get("/eventos-artistas", response_model=List[EventoArtista])
def get_eventos_artistas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_artista")
        eventos_artistas = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos_artistas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo evento-artista
@router.post("/evento-artista")
def create_evento_artista(evento_artista: EventoArtista):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO evento_artista (id_evento, id_artista) 
            VALUES (%s, %s)
            """,
            (
                evento_artista.id_evento,
                evento_artista.id_artista,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-artista creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un evento-artista por su id
@router.get("/evento-artista/{evento_artista_id}", response_model=EventoArtista)
def get_evento_artista(evento_artista_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evento_artista WHERE id = %s", (evento_artista_id,))
        evento_artista = cursor.fetchone()
        cursor.close()
        conn.close()
        if evento_artista is None:
            raise HTTPException(status_code=404, detail="Evento-artista no encontrado")
        return evento_artista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un evento-artista por su id
@router.put("/evento-artista/{evento_artista_id}")
def update_evento_artista(evento_artista_id: int, evento_artista: EventoArtista):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE evento_artista 
            SET id_evento = %s, id_artista = %s 
            WHERE id = %s
            """,
            (
                evento_artista.id_evento,
                evento_artista.id_artista,
                evento_artista_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-artista actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un evento-artista por su id
@router.delete("/evento-artista/{evento_artista_id}")
def delete_evento_artista(evento_artista_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evento_artista WHERE id = %s", (evento_artista_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Evento-artista eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    