from collections.abc import Sequence

from app.core.config import get_settings
from app.integrations.mock_data import MOCK_REFERENCE_CATALOG
from app.models.domain import ReferenceRecord


class GoogleSheetsReferenceRepository:
    """Cliente base para leer referencias desde Google Sheets.

    Si faltan credenciales, usa datos mock para permitir pruebas locales.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    def get_references(self, codes: Sequence[str]) -> list[ReferenceRecord]:
        if not self.settings.google_sheet_id or not self.settings.google_service_account_file:
            return [MOCK_REFERENCE_CATALOG[code] for code in codes if code in MOCK_REFERENCE_CATALOG]

        # Punto de extensión:
        # 1. autenticar con `gspread.service_account`
        # 2. abrir el spreadsheet
        # 3. mapear columnas a `ReferenceRecord`
        return [MOCK_REFERENCE_CATALOG[code] for code in codes if code in MOCK_REFERENCE_CATALOG]
