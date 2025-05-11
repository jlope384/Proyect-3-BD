from fastapi import APIRouter, HTTPException
from typing import List
from models import Usuario
from database import get_connection

router = APIRouter()

@router.get("/usuarios", response_model=List[Usuario])
def get_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email, id_rol FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/usuarios")
def create_usuario(usuario: Usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, email, id_rol) VALUES (%s, %s, %s)",
            (usuario.nombre, usuario.email, usuario.id_rol)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
