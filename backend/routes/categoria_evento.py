from fastapi import APIRouter, HTTPException
from typing import List
from models import CategoriaEvento
from database import get_connection

router = APIRouter()

#Devuelve todas las categorias de eventos en una lista
@router.get("/categorias-eventos", response_model=List[CategoriaEvento])
def get_categorias_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categoria_evento")
        categorias_eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return categorias_eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea una nueva categoria de evento
@router.post("/categoria-evento")
def create_categoria_evento(categoria_evento: CategoriaEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO categoria_evento (nombre) 
            VALUES (%s)
            """,
            (
                categoria_evento.nombre
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Categoria de evento creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve una categoria de evento por su id
@router.get("/categoria-evento/{categoria_evento_id}", response_model=CategoriaEvento)
def get_categoria_evento(categoria_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categoria_evento WHERE id = %s", (categoria_evento_id,))
        categoria_evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if categoria_evento is None:
            raise HTTPException(status_code=404, detail="Categoria de evento no encontrada")
        return categoria_evento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Actualiza una categoria de evento por su id
@router.put("/categoria-evento/{categoria_evento_id}")
def update_categoria_evento(categoria_evento_id: int, categoria_evento: CategoriaEvento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE categoria_evento 
            SET nombre = %s
            WHERE id = %s
            """,
            (
                categoria_evento.nombre,
                categoria_evento_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Categoria de evento actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Elimina una categoria de evento por su id
@router.delete("/categoria-evento/{categoria_evento_id}")
def delete_categoria_evento(categoria_evento_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categoria_evento WHERE id = %s", (categoria_evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Categoria de evento eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    