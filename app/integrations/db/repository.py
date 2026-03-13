from collections.abc import Sequence

from app.integrations.mock_data import MOCK_REFERENCE_CATALOG
from app.models.domain import ReferenceRecord


class DatabaseReferenceRepository:
    """Placeholder del repositorio SQL.

    En la siguiente iteración puede conectarse con SQLAlchemy y tablas reales.
    """

    def get_references(self, codes: Sequence[str]) -> list[ReferenceRecord]:
        return [MOCK_REFERENCE_CATALOG[code] for code in codes if code in MOCK_REFERENCE_CATALOG]
