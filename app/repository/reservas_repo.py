from typing import List, Optional
from app.models.reserva import Reserva


class InMemoryReservasRepository:
    """
    Repositorio en memoria: guarda las reservas en una lista.
    """

    def __init__(self):
        self._db: List[Reserva] = []

    def listar(self) -> List[Reserva]:
        return self._db

    def buscar_por_id(self, id_reserva: int) -> Optional[Reserva]:
        for r in self._db:
            if r.id_reserva == id_reserva:
                return r
        return None

    def guardar(self, reserva: Reserva) -> Reserva:
        self._db.append(reserva)
        return reserva