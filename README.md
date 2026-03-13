# Backend de guías y optimización de empaque

Backend base en FastAPI para:

1. recibir referencias y cantidades,
2. consultar información desde base de datos o Google Sheets,
3. calcular volumen automático,
4. optimizar el orden de empaque con `py3dbp`,
5. dejar lista la automatización de la transportadora para generar la guía.

## Stack inicial

- FastAPI
- Uvicorn
- py3dbp
- SQLAlchemy
- gspread + google-auth
- Pydantic Settings

## Estructura

- `app/api`: rutas HTTP
- `app/core`: configuración general
- `app/integrations`: conectores externos
- `app/models`: modelos de dominio
- `app/schemas`: contratos de entrada y salida
- `app/services`: lógica de negocio
- `tests`: pruebas base

## Arranque local

1. Crear o activar entorno virtual.
2. Instalar dependencias:
   - `pip install -r requirements.txt`
3. Copiar `.env.example` a `.env` y ajustar variables.
4. Ejecutar:
   - `uvicorn app.main:app --reload`

## Endpoint principal actual

- `POST /api/v1/references/optimize`

Ejemplo de payload:

```json
{
  "source": "mock",
  "items": [
    {"code": "REF-001", "quantity": 2},
    {"code": "REF-002", "quantity": 1}
  ]
}
```

## Estado actual

- Se dejó catálogo mock para pruebas.
- Se validó instalación y uso básico de `py3dbp`.
- Se dejaron puntos de extensión para Google Sheets, base de datos y automatización de transportadora.
