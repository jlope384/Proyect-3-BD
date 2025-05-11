from fastapi import APIRouter, HTTPException
from typing import List
from models import Asistente
from database import get_connection

router = APIRouter()

#Devuelve todos los asistentes en una lista
@router.get("/asistentes", response_model=List[Asistente])
def get_asistentes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asistente")
        asistentes = cursor.fetchall()
        cursor.close()
        conn.close()
        return asistentes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Crea un nuevo asistente
@router.post("/asistente")
def create_asistente(asistente: Asistente):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO asistente (nombre, correo, fecha_nacimiento) VALUES (%s, %s, %s)",
            (asistente.nombre, asistente.correo, asistente.fecha_nacimiento)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Asistente creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un asistente por su id
@router.get("/asistente/{asistente_id}", response_model=Asistente)
def get_asistente(asistente_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, correo, fecha_nacimiento FROM asistente WHERE id = %s", (asistente_id,))
        asistente = cursor.fetchone()
        cursor.close()
        conn.close()
        if asistente is None:
            raise HTTPException(status_code=404, detail="Asistente no encontrado")
        return asistente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un asistente por su id
@router.put("/asistente/{asistente_id}")
def update_asistente(asistente_id: int, asistente: Asistente):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE asistente SET nombre = %s, correo = %s, fecha_nacimiento = %s WHERE id = %s",
            (asistente.nombre, asistente.correo, asistente.fecha_nacimiento, asistente_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Asistente actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un asistente por su id
@router.delete("/asistente/{asistente_id}")
def delete_asistente(asistente_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM asistente WHERE id = %s", (asistente_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Asistente eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
