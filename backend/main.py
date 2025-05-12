from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import usuario, asistente, evento, entrada, artista, evento_patrocinador, evento_recurso, evento_artista, patrocinador, registro_asistencia, recurso, rol_usuario, calificacion_evento, lugar, ciudad, tipo_entrada, medio_pago, categoria_evento, tipo_evento, tema_evento

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return {"ping": "pong!"}

app.include_router(artista.router)
app.include_router(asistente.router)
app.include_router(calificacion_evento.router) 
app.include_router(entrada.router)
app.include_router(evento.router)
app.include_router(evento_patrocinador.router)
app.include_router(evento_recurso.router)
app.include_router(evento_artista.router)
app.include_router(patrocinador.router)
app.include_router(usuario.router)
app.include_router(registro_asistencia.router)
app.include_router(recurso.router)
app.include_router(rol_usuario.router)
app.include_router(lugar.router)
app.include_router(ciudad.router)
app.include_router(categoria_evento.router)
app.include_router(tipo_evento.router)
app.include_router(tema_evento.router)
app.include_router(tipo_entrada.router)
app.include_router(medio_pago.router)
