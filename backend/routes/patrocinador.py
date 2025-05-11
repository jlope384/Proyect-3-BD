from fastapi import APIRouter, HTTPException
from typing import List
from models import Patrocinador
from database import get_connection

router = APIRouter()

#Devuelve todos los patrocinadores en una lista
@router.get("/patrocinadores", response_model=List[Patrocinador])
def get_patrocinadores():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patrocinador")
        patrocinadores = cursor.fetchall()
        cursor.close()
        conn.close()
        return patrocinadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo patrocinador
@router.post("/patrocinador")
def create_patrocinador(patrocinador: Patrocinador):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patrocinador (nombre, tipo) VALUES (%s, %s)",
            (patrocinador.nombre, patrocinador.tipo)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patrocinador creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un patrocinador por su id
@router.get("/patrocinador/{patrocinador_id}", response_model=Patrocinador)
def get_patrocinador(patrocinador_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patrocinador WHERE id = %s", (patrocinador_id,))
        patrocinador = cursor.fetchone()
        cursor.close()
        conn.close()
        if patrocinador is None:
            raise HTTPException(status_code=404, detail="Patrocinador no encontrado")
        return patrocinador
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un patrocinador por su id
@router.put("/patrocinador/{patrocinador_id}")
def update_patrocinador(patrocinador_id: int, patrocinador: Patrocinador):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE patrocinador SET nombre = %s, tipo = %s WHERE id = %s",
            (patrocinador.nombre, patrocinador.tipo, patrocinador_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patrocinador actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un patrocinador por su id
@router.delete("/patrocinador/{patrocinador_id}")
def delete_patrocinador(patrocinador_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patrocinador WHERE id = %s", (patrocinador_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patrocinador eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un patrocinador por su id
@router.delete("/patrocinador/{patrocinador_id}")
def delete_patrocinador(patrocinador_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patrocinador WHERE id = %s", (patrocinador_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patrocinador eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
