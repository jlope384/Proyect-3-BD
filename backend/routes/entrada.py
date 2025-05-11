from fastapi import APIRouter, HTTPException
from typing import List
from models import Entrada
from database import get_connection

router = APIRouter()

#Devuelve todos los registros de asistencia en una lista
@router.get("/entradas", response_model=List[Entrada])
def get_entradas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entrada")
        entradas = cursor.fetchall()
        cursor.close()
        conn.close()
        return entradas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo registro de asistencia
@router.post("/entrada")
def create_entrada(entrada: Entrada):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entrada (id_evento, id_asistente, id_tipo_entrada, id_medio_pago, fecha_compra, precio_final) VALUES (%s, %s)",
            (entrada.id_evento, entrada.id_asistente, entrada.id_tipo_entrada, entrada.id_medio_pago, entrada.fecha_compra, entrada.precio_final)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Entrada creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un registro de asistencia por su id
@router.get("/entrada/{entrada_id}", response_model=Entrada)
def get_entrada(entrada_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entrada WHERE id = %s", (entrada_id,))
        entrada = cursor.fetchone()
        cursor.close()
        conn.close()
        if entrada is None:
            raise HTTPException(status_code=404, detail="Entrada no encontrada")
        return entrada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un registro de asistencia por su id
@router.put("/entrada/{entrada_id}")
def update_entrada(entrada_id: int, entrada: Entrada):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE entrada SET id_evento = %s, id_asistente = %s, id_tipo_entrada = %s, id_medio_pago = %s, fecha_compra = %s, precio_final = %s WHERE id = %s",
            (entrada.id_evento, entrada.id_asistente, entrada.id_tipo_entrada, entrada.id_medio_pago, entrada.fecha_compra, entrada.precio_final, entrada_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Entrada actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un registro de asistencia por su id
@router.delete("/entrada/{entrada_id}")
def delete_entrada(entrada_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entrada WHERE id = %s", (entrada_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Entrada eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
