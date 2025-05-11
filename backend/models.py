from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
    id_rol: int

class RolUsuario(BaseModel):
    id: Optional[int] = None
    nombre: str

class Ciudad(BaseModel):
    id: Optional[int] = None
    nombre: str
    departamento: str

class Lugar(BaseModel):
    id: Optional[int] = None
    nombre: str
    direccion: str
    id_ciudad: int
    capacidad: int

class CategoriaEvento(BaseModel):
    id: Optional[int] = None
    nombre: str

class TipoEvento(BaseModel):
    id: Optional[int] = None
    nombre: str

class TemaEvento(BaseModel):
    id: Optional[int] = None
    nombre: str

class TipoEntrada(BaseModel):
    id: Optional[int] = None
    descripcion: str
    precio_base: float

class MedioPago(BaseModel):
    id: Optional[int] = None
    metodo: str

class Asistente(BaseModel):
    id: Optional[int] = None
    nombre: str
    correo: str
    fecha_nacimiento: str  # ISO 8601 format: YYYY-MM-DD

class Evento(BaseModel):
    id: Optional[int] = None
    nombre: str
    fecha: str
    hora: str
    descripcion: Optional[str] = None
    id_lugar: int
    id_categoria_evento: int
    id_tipo_evento: int
    id_tema_evento: int
    id_usuario: int

class Entrada(BaseModel):
    id: Optional[int] = None
    id_evento: int
    id_asistente: int
    id_tipo_entrada: int
    id_medio_pago: int
    fecha_compra: str
    precio_final: float

class RegistroAsistencia(BaseModel):
    id: Optional[int] = None
    id_evento: int
    id_asistente: int
    fecha_hora: Optional[str] = None

class Artista(BaseModel):
    id: Optional[int] = None
    nombre: str
    tipo: str

class EventoArtista(BaseModel):
    id_evento: int
    id_artista: int

class Patrocinador(BaseModel):
    id: Optional[int] = None
    nombre: str
    tipo: Optional[str] = None

class EventoPatrocinador(BaseModel):
    id_evento: int
    id_patrocinador: int

class Recurso(BaseModel):
    id: Optional[int] = None
    nombre: str
    tipo: str

class EventoRecurso(BaseModel):
    id_evento: int
    id_recurso: int
    cantidad: int

class CalificacionEvento(BaseModel):
    id_evento: int
    id_asistente: int
    calificacion: int
    comentario: Optional[str] = None
