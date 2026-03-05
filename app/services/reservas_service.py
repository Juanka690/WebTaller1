from typing import List, Dict, Any
from fastapi import HTTPException
from pydantic import ValidationError
import json

from app.models.reserva import Reserva
from app.repository.reservas_repo import InMemoryReservasRepository


class ReservasService:
    def __init__(self, repo: InMemoryReservasRepository):
        self.repo = repo

    def listar_reservas(self) -> List[Reserva]:
        return self.repo.listar()

    def obtener_reserva(self, id_reserva: int) -> Reserva:
        reserva = self.repo.buscar_por_id(id_reserva)
        if reserva is None:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva

    def crear_reserva(self, reserva: Reserva) -> Reserva:
        if self.repo.buscar_por_id(reserva.id_reserva) is not None:
            raise HTTPException(status_code=409, detail="id_reserva ya existe")
        return self.repo.guardar(reserva)

    def crear_reservas_masivo(self, reservas_raw: List[Dict[str, Any]]) -> Dict[str, Any]:
        insertadas: List[Reserva] = []
        errores: List[Dict[str, Any]] = []

        for idx, raw in enumerate(reservas_raw):
            # 1) Validación Pydantic individual
            try:
                reserva = Reserva.model_validate(raw)
            except ValidationError as e:
                # ✅ esto SI es JSON serializable
                detalle_json = json.loads(e.json())
                errores.append({
                    "index": idx,
                    "id_reserva": raw.get("id_reserva") if isinstance(raw, dict) else None,
                    "tipo": "validacion",
                    "detalle": detalle_json
                })
                continue

            # 2) Duplicados
            if self.repo.buscar_por_id(reserva.id_reserva) is not None:
                errores.append({
                    "index": idx,
                    "id_reserva": reserva.id_reserva,
                    "tipo": "duplicado",
                    "detalle": "id_reserva ya existe"
                })
                continue

            # 3) Guardar
            self.repo.guardar(reserva)
            insertadas.append(reserva)

        return {
            "total_recibidas": len(reservas_raw),
            "total_insertadas": len(insertadas),
            "total_errores": len(errores),
            "insertadas": insertadas,
            "errores": errores
        }