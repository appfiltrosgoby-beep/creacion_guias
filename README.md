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

## Conectar referencias desde Google Sheets

1. Crea una cuenta de servicio en Google Cloud y descarga el JSON de credenciales.
2. Comparte tu hoja de Google con el correo de la cuenta de servicio (permiso de lector).
3. En `.env` configura:
  - `GOOGLE_SHEET_ID`: ID del archivo de Google Sheets.
  - `GOOGLE_SERVICE_ACCOUNT_FILE`: ruta local al JSON de la cuenta de servicio.
  - `GOOGLE_SHEET_WORKSHEET`: nombre de la pestaña (opcional; si se omite usa la primera).
4. En la pestaña define encabezados compatibles. Recomendados:
  - `code`, `name`, `length_cm`, `width_cm`, `height_cm`, `weight_kg`

Alias soportados para encabezados:
- `code`: `codigo`, `ref`, `sku`, `reference_code`
- `name`: `nombre`, `description`, `descripcion`
- `length_cm`: `length`, `largo_cm`, `largo`
- `width_cm`: `width`, `ancho_cm`, `ancho`
- `height_cm`: `height`, `alto_cm`, `alto`
- `weight_kg`: `weight`, `peso_kg`, `peso`

Para probar la fuente Google Sheets usa `source: "google_sheet"` en el payload.

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
