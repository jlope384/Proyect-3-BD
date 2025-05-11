from fastapi import APIRouter, HTTPException
from typing import List
from models import Recurso
from database import get_connection

router = APIRouter()

#Devuelve todos los recursos en una lista
@router.get("/recursos", response_model=List[Recurso])
def get_recursos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recurso")
        recursos = cursor.fetchall()
        cursor.close()
        conn.close()
        return recursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo recurso
@router.post("/recurso")
def create_recurso(recurso: Recurso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO recurso (nombre, tipo) VALUES (%s, %s)",
            (recurso.nombre, recurso.tipo)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Recurso creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un recurso por su id
@router.get("/recurso/{recurso_id}", response_model=Recurso)
def get_recurso(recurso_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recurso WHERE id = %s", (recurso_id,))
        recurso = cursor.fetchone()
        cursor.close()
        conn.close()
        if recurso is None:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        return recurso
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un recurso por su id
@router.put("/recurso/{recurso_id}")
def update_recurso(recurso_id: int, recurso: Recurso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recurso SET nombre = %s, tipo = %s WHERE id = %s",
            (recurso.nombre, recurso.tipo, recurso_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Recurso actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un recurso por su id
@router.delete("/recurso/{recurso_id}")
def delete_recurso(recurso_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recurso WHERE id = %s", (recurso_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Recurso eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    