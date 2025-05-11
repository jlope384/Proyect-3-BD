from fastapi import FastAPI
from routes import usuario

app = FastAPI()

@app.get("/")
def ping():
    return {"ping": "pong!"}

app.include_router(usuario.router)

