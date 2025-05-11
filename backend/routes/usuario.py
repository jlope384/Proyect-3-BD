from fastapi import APIRouter, HTTPException
from typing import List
from models import Usuario
from database import get_connection

router = APIRouter()

#Devuelve todos los usuarios en una lista
@router.get("/usuarios", response_model=List[Usuario])
def get_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Crea un nuevo usuario
@router.post("/usuario")
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

#Devuelve un usuario por su id
@router.get("/usuario/{usuario_id}", response_model=Usuario)
def get_usuario(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email, id_rol FROM usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un usuario por su id
@router.put("/usuario/{usuario_id}")
def update_usuario(usuario_id: int, usuario: Usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre = %s, email = %s, id_rol = %s WHERE id = %s",
            (usuario.nombre, usuario.email, usuario.id_rol, usuario_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un usuario por su id
@router.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve todos los usuarios por su rol
@router.get("/usuarios/rol/{rol_id}", response_model=List[Usuario])
def get_usuarios_by_rol(rol_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, email, id_rol FROM usuario WHERE id_rol = %s", (rol_id,))
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
