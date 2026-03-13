from app.models.domain import Dimensions, ReferenceRecord, ShipmentBox

MOCK_REFERENCE_CATALOG: dict[str, ReferenceRecord] = {
    "REF-001": ReferenceRecord(
        code="REF-001",
        name="Caja organizadora pequeña",
        dimensions=Dimensions(length_cm=20, width_cm=15, height_cm=10),
        weight_kg=1.2,
    ),
    "REF-002": ReferenceRecord(
        code="REF-002",
        name="Set vasos x6",
        dimensions=Dimensions(length_cm=18, width_cm=12, height_cm=12),
        weight_kg=0.9,
    ),
    "REF-003": ReferenceRecord(
        code="REF-003",
        name="Contenedor hermético",
        dimensions=Dimensions(length_cm=28, width_cm=20, height_cm=14),
        weight_kg=1.8,
    ),
}

DEFAULT_BOXES: list[ShipmentBox] = [
    ShipmentBox(
        code="BOX-S",
        dimensions=Dimensions(length_cm=30, width_cm=25, height_cm=20),
        max_weight_kg=10,
    ),
    ShipmentBox(
        code="BOX-M",
        dimensions=Dimensions(length_cm=45, width_cm=35, height_cm=30),
        max_weight_kg=20,
    ),
    ShipmentBox(
        code="BOX-L",
        dimensions=Dimensions(length_cm=60, width_cm=45, height_cm=40),
        max_weight_kg=30,
    ),
]
