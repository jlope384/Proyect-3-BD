from fastapi import APIRouter, HTTPException
from typing import List
from models import RolUsuario
from database import get_connection

router = APIRouter()

#Devuelve todos los roles de usuario en una lista
@router.get("/roles-usuario", response_model=List[RolUsuario])
def get_roles_usuario():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rol_usuario")
        roles_usuario = cursor.fetchall()
        cursor.close()
        conn.close()
        return roles_usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Crea un nuevo rol de usuario
@router.post("/rol-usuario")
def create_rol_usuario(rol_usuario: RolUsuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO rol_usuario (nombre) 
            VALUES (%s)
            """,
            (
                rol_usuario.nombre,
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Rol de usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve un rol de usuario por su id
@router.get("/rol-usuario/{rol_usuario_id}", response_model=RolUsuario)
def get_rol_usuario(rol_usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rol_usuario WHERE id = %s", (rol_usuario_id,))
        rol_usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if rol_usuario is None:
            raise HTTPException(status_code=404, detail="Rol de usuario no encontrado")
        return rol_usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Actualiza un rol de usuario por su id
@router.put("/rol-usuario/{rol_usuario_id}")
def update_rol_usuario(rol_usuario_id: int, rol_usuario: RolUsuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE rol_usuario 
            SET nombre = %s 
            WHERE id = %s
            """,
            (
                rol_usuario.nombre,
                rol_usuario_id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Rol de usuario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Elimina un rol de usuario por su id
@router.delete("/rol-usuario/{rol_usuario_id}")
def delete_rol_usuario(rol_usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rol_usuario WHERE id = %s", (rol_usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Rol de usuario eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))