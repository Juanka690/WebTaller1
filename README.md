# Microservicio de Reservas (FastAPI + Pydantic)

API para registrar reservas y listarlas.  
Las reservas se guardan en memoria (lista), no hay base de datos.

## Requisitos
- Python 3.10+

## Instalación
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt