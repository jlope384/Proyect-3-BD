from fastapi import APIRouter, HTTPException
from typing import List
from models import TipoEntrada
from database import get_connection

router = APIRouter()

#Devuelve todos los tipos de entrada en una lista
@router.get("/tipos-entrada", response_model=List[TipoEntrada])
def get_tipos_entrada():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_entrada")
        tipos_entrada = cursor.fetchall()
        cursor.close()
        conn.close()
        return tipos_entrada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo tipo de entrada
@router.post("/tipo-entrada")
def create_tipo_entrada(tipo_entrada: TipoEntrada):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tipo_entrada (descripcion, precio_base) 
            VALUES (%s)
            """,
            (
                tipo_entrada.descripcion,
                tipo_entrada.precio_base,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de entrada creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un tipo de entrada por su id
@router.get("/tipo-entrada/{tipo_entrada_id}", response_model=TipoEntrada)
def get_tipo_entrada(tipo_entrada_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_entrada WHERE id = %s", (tipo_entrada_id,))
        tipo_entrada = cursor.fetchone()
        cursor.close()
        conn.close()
        if tipo_entrada is None:
            raise HTTPException(status_code=404, detail="Tipo de entrada no encontrado")
        return tipo_entrada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un tipo de entrada por su id
@router.put("/tipo-entrada/{tipo_entrada_id}")
def update_tipo_entrada(tipo_entrada_id: int, tipo_entrada: TipoEntrada):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tipo_entrada 
            SET descripcion = %s, precio_base = %s
            WHERE id = %s
            """,
            (
                tipo_entrada.descripcion,
                tipo_entrada.precio_base,
                tipo_entrada_id,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de entrada actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un tipo de entrada por su id
@router.delete("/tipo-entrada/{tipo_entrada_id}")
def delete_tipo_entrada(tipo_entrada_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo_entrada WHERE id = %s", (tipo_entrada_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tipo de entrada eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    