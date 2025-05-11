from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    email: str
    id_rol: int
