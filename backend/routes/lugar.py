from fastapi import APIRouter, HTTPException
from typing import List
from models import Lugar
from database import get_connection

router = APIRouter()
#Devuelve todos los lugares en una lista
@router.get("/lugares", response_model=List[Lugar])
def get_lugares():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lugar")
        lugares = cursor.fetchall()
        cursor.close()
        conn.close()
        return lugares
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo lugar
@router.post("/lugar")
def create_lugar(lugar: Lugar):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO lugar (nombre, direccion, id_ciudad, capacidad) 
            VALUES (%s, %s, %s)
            """,
            (
                lugar.nombre,
                lugar.direccion,
                lugar.id_ciudad,
                lugar.capacidad,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Lugar creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un lugar por su id
@router.get("/lugar/{lugar_id}", response_model=Lugar)
def get_lugar(lugar_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lugar WHERE id = %s", (lugar_id,))
        lugar = cursor.fetchone()
        cursor.close()
        conn.close()
        if lugar is None:
            raise HTTPException(status_code=404, detail="Lugar no encontrado")
        return lugar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un lugar por su id
@router.put("/lugar/{lugar_id}")
def update_lugar(lugar_id: int, lugar: Lugar):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE lugar 
            SET nombre = %s, direccion = %s, id_ciudad = %s, capacidad = %s 
            WHERE id = %s
            """,
            (
                lugar.nombre,
                lugar.direccion,
                lugar.id_ciudad,
                lugar.capacidad,
                lugar_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Lugar actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un lugar por su id
@router.delete("/lugar/{lugar_id}")
def delete_lugar(lugar_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lugar WHERE id = %s", (lugar_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Lugar eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

