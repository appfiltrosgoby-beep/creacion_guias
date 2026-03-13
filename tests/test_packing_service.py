from app.schemas.reference import DataSourceType, PackingRequest, PackingRequestItem
from app.services.packing_service import PackingService


def test_optimize_returns_boxes_and_volume() -> None:
    service = PackingService()

    result = service.optimize(
        PackingRequest(
            source=DataSourceType.mock,
            items=[
                PackingRequestItem(code="REF-001", quantity=2),
                PackingRequestItem(code="REF-002", quantity=1),
            ],
        )
    )

    assert result.total_requested_items == 3
    assert result.total_volume_cm3 > 0
    assert result.references
    assert result.boxes_used
    assert result.missing_codes == []
