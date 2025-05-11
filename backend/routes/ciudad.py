from fastapi import APIRouter, HTTPException
from typing import List
from models import Ciudad
from database import get_connection

router = APIRouter()

#Devuelve todas las ciudades en una lista
@router.get("/ciudades", response_model=List[Ciudad])
def get_ciudades():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ciudad")
        ciudades = cursor.fetchall()
        cursor.close()
        conn.close()
        return ciudades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea una nueva ciudad
@router.post("/ciudad")
def create_ciudad(ciudad: Ciudad):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ciudad (nombre, departamento) 
            VALUES (%s, %s)
            """,
            (
                ciudad.nombre,
                ciudad.departamento,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Ciudad creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve una ciudad por su id
@router.get("/ciudad/{ciudad_id}", response_model=Ciudad)
def get_ciudad(ciudad_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ciudad WHERE id = %s", (ciudad_id,))
        ciudad = cursor.fetchone()
        cursor.close()
        conn.close()
        if ciudad is None:
            raise HTTPException(status_code=404, detail="Ciudad no encontrada")
        return ciudad
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza una ciudad por su id
@router.put("/ciudad/{ciudad_id}")
def update_ciudad(ciudad_id: int, ciudad: Ciudad):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE ciudad 
            SET nombre = %s, departamento = %s 
            WHERE id = %s
            """,
            (
                ciudad.nombre,
                ciudad.departamento,
                ciudad_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Ciudad actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina una ciudad por su id
@router.delete("/ciudad/{ciudad_id}")
def delete_ciudad(ciudad_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ciudad WHERE id = %s", (ciudad_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Ciudad eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))