from collections.abc import Sequence

from app.integrations.db.repository import DatabaseReferenceRepository
from app.integrations.google_sheets.client import GoogleSheetsReferenceRepository
from app.integrations.mock_data import MOCK_REFERENCE_CATALOG
from app.models.domain import ReferenceRecord
from app.schemas.reference import DataSourceType


class CatalogService:
    def __init__(self) -> None:
        self.database_repository = DatabaseReferenceRepository()
        self.google_sheets_repository = GoogleSheetsReferenceRepository()

    def get_references(self, codes: Sequence[str], source: DataSourceType) -> list[ReferenceRecord]:
        unique_codes = list(dict.fromkeys(code.upper() for code in codes))

        if source == DataSourceType.database:
            return self.database_repository.get_references(unique_codes)
        if source == DataSourceType.google_sheet:
            return self.google_sheets_repository.get_references(unique_codes)

        return [MOCK_REFERENCE_CATALOG[code] for code in unique_codes if code in MOCK_REFERENCE_CATALOG]
