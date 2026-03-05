from datetime import date, time
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class EstadoReserva(str, Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"


class Reserva(BaseModel):
    id_reserva: int = Field(..., ge=1)
    id_sala: int = Field(..., ge=1)
    id_usuario: int = Field(..., ge=1)

    fecha: date
    hora_inicio: time
    hora_fin: time

    personas: int = Field(..., ge=1, le=500)
    estado: EstadoReserva

    @model_validator(mode="after")
    def validar_horas(self):
        # Regla básica: la hora fin debe ser mayor a la hora inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("hora_fin debe ser mayor que hora_inicio")
        return self