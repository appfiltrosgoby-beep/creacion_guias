from collections.abc import Sequence
import logging

from app.core.config import Settings, get_settings
from app.integrations.mock_data import MOCK_REFERENCE_CATALOG
from app.models.domain import Dimensions, ReferenceRecord

logger = logging.getLogger(__name__)


class GoogleSheetsReferenceRepository:
    """Cliente base para leer referencias desde Google Sheets.

    Si faltan credenciales, usa datos mock para permitir pruebas locales.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def get_references(self, codes: Sequence[str]) -> list[ReferenceRecord]:
        unique_codes = list(dict.fromkeys(code.upper() for code in codes))
        if not unique_codes:
            return []

        if not self.settings.google_sheet_id or not self.settings.google_service_account_file:
            return [MOCK_REFERENCE_CATALOG[code] for code in unique_codes if code in MOCK_REFERENCE_CATALOG]

        try:
            rows = self._fetch_rows()
        except Exception as error:  # pragma: no cover
            logger.warning("No fue posible leer Google Sheets. Se usa fallback mock.", exc_info=error)
            return [MOCK_REFERENCE_CATALOG[code] for code in unique_codes if code in MOCK_REFERENCE_CATALOG]

        references_by_code: dict[str, ReferenceRecord] = {}
        for row in rows:
            reference = self._build_reference_record(row)
            if reference is None:
                continue
            references_by_code[reference.code.upper()] = reference

        return [references_by_code[code] for code in unique_codes if code in references_by_code]

    def _fetch_rows(self) -> list[dict[str, object]]:
        import gspread

        client = gspread.service_account(filename=self.settings.google_service_account_file)
        spreadsheet = client.open_by_key(self.settings.google_sheet_id)

        worksheet_name = self.settings.google_sheet_worksheet.strip()
        worksheet = spreadsheet.worksheet(worksheet_name) if worksheet_name else spreadsheet.sheet1
        return worksheet.get_all_records()

    def _build_reference_record(self, raw_row: dict[str, object]) -> ReferenceRecord | None:
        normalized_row = {
            self._normalize_key(key): value
            for key, value in raw_row.items()
            if isinstance(key, str)
        }

        code = self._pick_value(normalized_row, ["code", "codigo", "ref", "sku", "reference_code"])
        name = self._pick_value(normalized_row, ["name", "nombre", "description", "descripcion"]) or code
        length_cm = self._to_positive_float(
            self._pick_value(normalized_row, ["length_cm", "length", "largo_cm", "largo"])
        )
        width_cm = self._to_positive_float(
            self._pick_value(normalized_row, ["width_cm", "width", "ancho_cm", "ancho"])
        )
        height_cm = self._to_positive_float(
            self._pick_value(normalized_row, ["height_cm", "height", "alto_cm", "alto"])
        )
        weight_kg = self._to_positive_float(
            self._pick_value(normalized_row, ["weight_kg", "weight", "peso_kg", "peso"])
        )

        if not code or not name or None in (length_cm, width_cm, height_cm, weight_kg):
            return None

        return ReferenceRecord(
            code=code.upper(),
            name=name,
            dimensions=Dimensions(
                length_cm=length_cm,
                width_cm=width_cm,
                height_cm=height_cm,
            ),
            weight_kg=weight_kg,
        )

    def _pick_value(self, row: dict[str, object], aliases: list[str]) -> str:
        for alias in aliases:
            value = row.get(alias)
            if value is None:
                continue

            text = str(value).strip()
            if text:
                return text
        return ""

    def _normalize_key(self, key: str) -> str:
        return key.strip().lower().replace(" ", "_")

    def _to_positive_float(self, value: str) -> float | None:
        if not value:
            return None

        normalized = value.replace(",", ".")
        try:
            number = float(normalized)
        except ValueError:
            return None

        return number if number > 0 else None
