from fastapi import APIRouter, HTTPException
from typing import List
from models import MedioPago
from database import get_connection

router = APIRouter()

#Devuelve todos los medios de pago en una lista
@router.get("/medios-pago", response_model=List[MedioPago])
def get_medios_pago():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medio_pago")
        medios_pago = cursor.fetchall()
        cursor.close()
        conn.close()
        return medios_pago
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo medio de pago
@router.post("/medio-pago")
def create_medio_pago(medio_pago: MedioPago):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO medio_pago (metodo) 
            VALUES (%s)
            """,
            (
                medio_pago.metodo,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Medio de pago creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un medio de pago por su id
@router.get("/medio-pago/{medio_pago_id}", response_model=MedioPago)
def get_medio_pago(medio_pago_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medio_pago WHERE id = %s", (medio_pago_id,))
        medio_pago = cursor.fetchone()
        cursor.close()
        conn.close()
        if medio_pago is None:
            raise HTTPException(status_code=404, detail="Medio de pago no encontrado")
        return medio_pago
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un medio de pago por su id
@router.put("/medio-pago/{medio_pago_id}")
def update_medio_pago(medio_pago_id: int, medio_pago: MedioPago):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE medio_pago 
            SET metodo = %s
            WHERE id = %s
            """,
            (
                medio_pago.metodo,
                medio_pago_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Medio de pago actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un medio de pago por su id
@router.delete("/medio-pago/{medio_pago_id}")
def delete_medio_pago(medio_pago_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medio_pago WHERE id = %s", (medio_pago_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Medio de pago eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    