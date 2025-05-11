from fastapi import APIRouter, HTTPException
from typing import List
from models import Artista
from database import get_connection

router = APIRouter()

#Devuelve todos los artistas en una lista
@router.get("/artistas", response_model=List[Artista])
def get_artistas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artista")
        artistas = cursor.fetchall()
        cursor.close()
        conn.close()
        return artistas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo artista
@router.post("/artista")
def create_artista(artista: Artista):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO artista (nombre, tipo) VALUES (%s, %s, %s)",
            (artista.nombre, artista.tipo)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Artista creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Devuelve un artista por su id
@router.get("/artista/{artista_id}", response_model=Artista)
def get_artista(artista_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artista WHERE id = %s", (artista_id,))
        artista = cursor.fetchone()
        cursor.close()
        conn.close()
        if artista is None:
            raise HTTPException(status_code=404, detail="Artista no encontrado")
        return artista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un artista por su id
@router.put("/artista/{artista_id}")
def update_artista(artista_id: int, artista: Artista):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE artista SET nombre = %s, tipo = %s WHERE id = %s",
            (artista.nombre, artista.tipo, artista_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Artista actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un artista por su id
@router.delete("/artista/{artista_id}")
def delete_artista(artista_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM artista WHERE id = %s", (artista_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Artista eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

