from fastapi import FastAPI
from routes import usuario, asistente, evento, entrada

app = FastAPI()

@app.get("/")
def ping():
    return {"ping": "pong!"}

app.include_router(usuario.router)
app.include_router(asistente.router)
app.include_router(evento.router)
app.include_router(entrada.router)