from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.models.reserva import Reserva
from app.repository.reservas_repo import InMemoryReservasRepository
from app.services.reservas_service import ReservasService

router = APIRouter(prefix="", tags=["Reservas"])

# Dependencias en memoria
_repo = InMemoryReservasRepository()
_service = ReservasService(_repo)


class ReservasMasivoRequest(BaseModel):
    reservas: List[Dict[str, Any]] = Field(..., description="Lista de reservas en JSON (pueden venir válidas e inválidas)")


class ReservasMasivoResponse(BaseModel):
    total_recibidas: int
    total_insertadas: int
    total_errores: int
    insertadas: List[Reserva]
    errores: List[Dict[str, Any]]


@router.post("/reservas", response_model=Reserva, status_code=201)
def crear_reserva(reserva: Reserva):
    return _service.crear_reserva(reserva)


@router.post("/reservas/masivo", response_model=ReservasMasivoResponse, status_code=200)
def crear_reservas_masivo(payload: ReservasMasivoRequest):
    return _service.crear_reservas_masivo(payload.reservas)


@router.get("/reservas", response_model=List[Reserva])
def listar_reservas():
    return _service.listar_reservas()


@router.get("/reservas/{id_reserva}", response_model=Reserva)
def obtener_reserva_por_id(id_reserva: int):
    return _service.obtener_reserva(id_reserva)