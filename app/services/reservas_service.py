from typing import List
from fastapi import HTTPException

from app.models.reserva import Reserva
from app.repository.reservas_repo import InMemoryReservasRepository


class ReservasService:
    """
    Lógica de negocio:
    - Evitar id_reserva duplicado
    """

    def __init__(self, repo: InMemoryReservasRepository):
        self.repo = repo

    def listar_reservas(self) -> List[Reserva]:
        return self.repo.listar()

    def crear_reserva(self, reserva: Reserva) -> Reserva:
        existente = self.repo.buscar_por_id(reserva.id_reserva)
        if existente is not None:
            raise HTTPException(status_code=409, detail="id_reserva ya existe")

        return self.repo.guardar(reserva)