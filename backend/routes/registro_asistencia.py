from fastapi import APIRouter, HTTPException
from typing import List
from models import RegistroAsistencia
from database import get_connection

router = APIRouter()

#Devuelve todos los registros de asistencia en una lista
@router.get("/registros_asistencia", response_model=List[RegistroAsistencia])
def get_registros_asistencia():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registro_asistencia")
        registros_asistencia = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros_asistencia
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo registro de asistencia
@router.post("/registro_asistencia")
def create_registro_asistencia(registro_asistencia: RegistroAsistencia):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO registro_asistencia (id_evento, id_asistente, fecha_hora) 
            VALUES (%s, %s, %s)
            """,
            (
                registro_asistencia.id_evento,
                registro_asistencia.id_asistente,
                registro_asistencia.fecha_hora,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Registro de asistencia creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un registro de asistencia por su id
@router.get("/registro_asistencia/{registro_asistencia_id}", response_model=RegistroAsistencia)
def get_registro_asistencia(registro_asistencia_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registro_asistencia WHERE id = %s", (registro_asistencia_id,))
        registro_asistencia = cursor.fetchone()
        cursor.close()
        conn.close()
        if registro_asistencia is None:
            raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
        return registro_asistencia
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un registro de asistencia por su id
@router.put("/registro_asistencia/{registro_asistencia_id}")
def update_registro_asistencia(registro_asistencia_id: int, registro_asistencia: RegistroAsistencia):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE registro_asistencia 
            SET id_evento = %s, id_asistente = %s, fecha_hora = %s 
            WHERE id = %s
            """,
            (
                registro_asistencia.id_evento,
                registro_asistencia.id_asistente,
                registro_asistencia.fecha_hora,
                registro_asistencia_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Registro de asistencia actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un registro de asistencia por su id
@router.delete("/registro_asistencia/{registro_asistencia_id}")
def delete_registro_asistencia(registro_asistencia_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registro_asistencia WHERE id = %s", (registro_asistencia_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Registro de asistencia eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
