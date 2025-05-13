from fastapi import APIRouter, HTTPException
from models import Asistente
from database import get_connection

router = APIRouter(prefix="/api")

@router.post("/asistentes")
def crear_asistente(asistente: Asistente):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO asistente (nombre, correo, fecha_nacimiento) VALUES (%s, %s, %s) RETURNING id",
            (asistente.nombre, asistente.correo, asistente.fecha_nacimiento)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": new_id, **asistente.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/asistentes/{asistente_id}")
def actualizar_asistente(asistente_id: int, asistente: Asistente):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE asistente SET nombre = %s, correo = %s, fecha_nacimiento = %s WHERE id = %s",
            (asistente.nombre, asistente.correo, asistente.fecha_nacimiento, asistente_id)
        )
        conn.commit()
        return {"message": "Asistente actualizado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()