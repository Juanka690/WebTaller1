from typing import List
from fastapi import APIRouter

from app.models.reserva import Reserva
from app.repository.reservas_repo import InMemoryReservasRepository
from app.services.reservas_service import ReservasService

router = APIRouter(prefix="", tags=["Reservas"])

# Dependencias simples (en memoria)
_repo = InMemoryReservasRepository()
_service = ReservasService(_repo)


@router.post("/reservas", response_model=Reserva, status_code=201)
def crear_reserva(reserva: Reserva):
    return _service.crear_reserva(reserva)


@router.get("/reservas", response_model=List[Reserva])
def listar_reservas():
    return _service.listar_reservas()