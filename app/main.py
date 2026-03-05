from fastapi import FastAPI
from app.api.reservas_routes import router as reservas_router

app = FastAPI(
    title="Microservicio de Reservas",
    version="1.0.0",
    description="API básica para crear y consultar reservas (almacenamiento en memoria).",
)

@app.get("/")
def health():
    return {"status": "ok", "message": "Servicio de reservas activo"}

app.include_router(reservas_router)