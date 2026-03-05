# Microservicio de Reservas — FastAPI + Pydantic (Laboratorio 1)

Este proyecto implementa un **microservicio de reservas de salas** usando **FastAPI** (para exponer la API) y **Pydantic** (para modelar y validar datos).
El sistema permite **crear reservas**, **listar todas**, **consultar por ID** y **cargar reservas en masa** mediante un JSON.

✅ Enfoque educativo: las reservas se guardan en **memoria (RAM)**, sin base de datos.  
⚠️ Importante: si reinicias el servidor, se pierden los datos guardados.

---

## Integrantes

- **Juan Camilo Cardona Sánchez**
- **Miguel Castaño Moya**

---

## Tecnologías usadas

- **Python 3.10+**
- **FastAPI**
- **Pydantic v2**
- **Uvicorn**

---

## Estructura del proyecto

```text
reservas-fastapi/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ reservas_routes.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ reserva.py
│  ├─ repository/
│  │  ├─ __init__.py
│  │  └─ reservas_repo.py
│  └─ services/
│     ├─ __init__.py
│     └─ reservas_service.py
├─ data/
│  ├─ reservas_prueba.json
│  └─ reservas_masivo_pruebas.json
├─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## Modelo de datos: `Reserva`

Una reserva tiene los siguientes campos:

- `id_reserva` (int, >= 1)
- `id_sala` (int, >= 1)
- `id_usuario` (int, >= 1)
- `fecha` (formato `YYYY-MM-DD`)
- `hora_inicio` (formato `HH:MM:SS`)
- `hora_fin` (formato `HH:MM:SS`)
- `personas` (int, >= 1)
- `estado` (solo: `pendiente`, `confirmada`, `cancelada`)

### Validaciones aplicadas
- `hora_fin` **debe ser mayor** que `hora_inicio`
- `personas` **debe ser >= 1**
- `estado` solo permite: `pendiente`, `confirmada`, `cancelada`

---

## Cómo correr el proyecto

### 1) Crear y activar entorno virtual

**Windows (PowerShell):**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3) Ejecutar el servidor
```bash
uvicorn app.main:app --reload
```

---

## Interfaz automática de FastAPI (Swagger)

FastAPI genera una interfaz automática para probar los endpoints (lo requerido en el taller):

- Swagger UI: `http://127.0.0.1:8000/docs`

En Swagger puedes:
1. Abrir un endpoint.
2. Presionar **Try it out**.
3. Pegar el JSON (si aplica).
4. Presionar **Execute**.
5. Ver el **status code** y el **response body**.

---

## Archivos de prueba (`data/`)

### `data/reservas_prueba.json`
Contiene ejemplos organizados en:
- `validas`: para probar `POST /reservas` (una por una).
- `invalidas`: para comprobar validaciones (deben fallar con 422).

📌 **No se “ejecuta”** como programa: se **copia y pega** el objeto JSON desde este archivo en Swagger (`/docs`) dentro del body del endpoint.

### `data/reservas_masivo_pruebas.json`
Diseñado para el endpoint `POST /reservas/masivo`. Su formato requerido es:

```json
{
  "reservas": [
    { "id_reserva": 1, "id_sala": 101, "id_usuario": 9001, "fecha": "2026-03-10",
      "hora_inicio": "08:00:00", "hora_fin": "10:00:00", "personas": 25, "estado": "pendiente" }
  ]
}
```

📌 En carga masiva:
- Se guardan las reservas válidas.
- Las inválidas se reportan en `errores`.
- La carga **no se cae** por un registro inválido.

---

## Base URL

```text
http://127.0.0.1:8000
```

---

## Resumen de Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Healthcheck del servicio |
| POST | `/reservas` | Crear una reserva individual |
| POST | `/reservas/masivo` | Cargar muchas reservas en un solo request |
| GET | `/reservas` | Listar todas las reservas |
| GET | `/reservas/{id_reserva}` | Consultar una reserva por ID |

---

## Detalle de Endpoints (con respuestas)

### 1) Healthcheck
**GET** `/`

**Respuesta (200):**
```json
{
  "status": "ok",
  "message": "Servicio de reservas activo"
}
```

---

### 2) Crear una reserva
**POST** `/reservas`

**Body ejemplo válido:**
```json
{
  "id_reserva": 1,
  "id_sala": 101,
  "id_usuario": 9001,
  "fecha": "2026-03-10",
  "hora_inicio": "08:00:00",
  "hora_fin": "10:00:00",
  "personas": 25,
  "estado": "pendiente"
}
```

**Respuesta (201 Created):**
```json
{
  "id_reserva": 1,
  "id_sala": 101,
  "id_usuario": 9001,
  "fecha": "2026-03-10",
  "hora_inicio": "08:00:00",
  "hora_fin": "10:00:00",
  "personas": 25,
  "estado": "pendiente"
}
```

**Errores comunes:**
- **409 Conflict** (ID duplicado):
```json
{ "detail": "id_reserva ya existe" }
```

- **422 Unprocessable Entity** (datos inválidos):  
Ejemplos: fecha mal escrita, `estado` inválido, `personas = 0`, `hora_fin <= hora_inicio`, etc.

---

### 3) Cargar reservas en masa
**POST** `/reservas/masivo`

**Body (formato obligatorio):**
```json
{
  "reservas": [
    {
      "id_reserva": 10,
      "id_sala": 100,
      "id_usuario": 1,
      "fecha": "2026-03-10",
      "hora_inicio": "08:00:00",
      "hora_fin": "09:00:00",
      "personas": 3,
      "estado": "pendiente"
    }
  ]
}
```

**Respuesta (200 OK) — ejemplo de salida:**
```json
{
  "total_recibidas": 3,
  "total_insertadas": 2,
  "total_errores": 1,
  "insertadas": [
    {
      "id_reserva": 10,
      "id_sala": 100,
      "id_usuario": 1,
      "fecha": "2026-03-10",
      "hora_inicio": "08:00:00",
      "hora_fin": "09:00:00",
      "personas": 3,
      "estado": "pendiente"
    }
  ],
  "errores": [
    {
      "index": 2,
      "id_reserva": 12,
      "tipo": "validacion",
      "detalle": [
        {
          "type": "value_error",
          "loc": [],
          "msg": "Value error, hora_fin debe ser mayor que hora_inicio"
        }
      ]
    }
  ]
}
```

**Notas:**
- `index`: posición del elemento dentro del arreglo `reservas`.
- `tipo`: `validacion` o `duplicado`.
- `detalle`: explicación del error (serializable en JSON).

---

### 4) Listar todas las reservas
**GET** `/reservas`

**Respuesta (200 OK):**
```json
[
  {
    "id_reserva": 1,
    "id_sala": 101,
    "id_usuario": 9001,
    "fecha": "2026-03-10",
    "hora_inicio": "08:00:00",
    "hora_fin": "10:00:00",
    "personas": 25,
    "estado": "pendiente"
  }
]
```

---

### 5) Consultar una reserva por ID
**GET** `/reservas/{id_reserva}`

Ejemplo: `GET /reservas/2`

**Respuesta (200 OK):**
```json
{
  "id_reserva": 2,
  "id_sala": 202,
  "id_usuario": 9002,
  "fecha": "2026-03-11",
  "hora_inicio": "14:00:00",
  "hora_fin": "16:30:00",
  "personas": 10,
  "estado": "confirmada"
}
```

Si no existe:
- **404 Not Found**
```json
{ "detail": "Reserva no encontrada" }
```

---

## Flujo recomendado de prueba (para sustentación)

1) Ejecutar el servidor:
```bash
uvicorn app.main:app --reload
```

2) Abrir Swagger:
```text
http://127.0.0.1:8000/docs
```

3) Probar en este orden:
- `POST /reservas/masivo` (pega el contenido de `data/reservas_masivo_pruebas.json`)
- `GET /reservas` (ver todas las reservas guardadas)
- `GET /reservas/{id}` (buscar una reserva específica)
- `POST /reservas` con un `id_reserva` repetido (demostrar **409**)
- Probar un caso inválido (demostrar **422**)

---
