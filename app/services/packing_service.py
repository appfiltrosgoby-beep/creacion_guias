from collections import Counter
from decimal import Decimal

from py3dbp import Bin, Item, Packer

from app.integrations.mock_data import DEFAULT_BOXES
from app.models.domain import ReferenceRecord, ShipmentBox
from app.schemas.reference import (
    BoxPlanResponse,
    DataSourceType,
    DimensionResponse,
    PackedItemResponse,
    PackingRequest,
    PackingResponse,
    ReferenceResolvedResponse,
)
from app.services.catalog_service import CatalogService


class PackingService:
    def __init__(self, catalog_service: CatalogService | None = None) -> None:
        self.catalog_service = catalog_service or CatalogService()

    def optimize(self, request: PackingRequest) -> PackingResponse:
        requested_codes = [item.code.upper() for item in request.items]
        requested_quantities = Counter()
        for item in request.items:
            requested_quantities[item.code.upper()] += item.quantity

        references = self.catalog_service.get_references(requested_codes, request.source)
        references_by_code = {reference.code.upper(): reference for reference in references}
        missing_codes = [code for code in requested_quantities if code not in references_by_code]

        resolved_references = [
            self._build_reference_response(reference, requested_quantities[reference.code.upper()])
            for reference in references
        ]

        boxes = self._select_boxes(request.box_type)
        packer = Packer()
        for box in boxes:
            packer.add_bin(
                Bin(
                    box.code,
                    box.dimensions.length_cm,
                    box.dimensions.width_cm,
                    box.dimensions.height_cm,
                    box.max_weight_kg,
                )
            )

        for code, quantity in requested_quantities.items():
            reference = references_by_code.get(code)
            if reference is None:
                continue

            for index in range(quantity):
                packer.add_item(
                    Item(
                        f"{code}__{index + 1}",
                        reference.dimensions.length_cm,
                        reference.dimensions.width_cm,
                        reference.dimensions.height_cm,
                        reference.weight_kg,
                    )
                )

        if packer.bins:
            packer.pack(bigger_first=True, distribute_items=True)

        boxes_used = [self._build_box_response(bin_result, boxes) for bin_result in packer.bins]
        boxes_used = [box for box in boxes_used if box.fitted_items or box.unfitted_items]

        total_requested_items = sum(requested_quantities.values())
        total_volume_cm3 = sum(item.dimensions.volume_cm3 * quantity for item, quantity in [
            (references_by_code[code], quantity)
            for code, quantity in requested_quantities.items()
            if code in references_by_code
        ])
        total_weight_kg = sum(item.weight_kg * quantity for item, quantity in [
            (references_by_code[code], quantity)
            for code, quantity in requested_quantities.items()
            if code in references_by_code
        ])

        notes = [
            "La automatización de la transportadora queda preparada como siguiente fase.",
            "Google Sheets y base de datos usan un adaptador mock hasta conectar credenciales reales.",
        ]
        if request.box_type:
            notes.append(f"Filtrado de caja aplicado: {request.box_type}.")

        return PackingResponse(
            source=request.source,
            total_requested_items=total_requested_items,
            total_volume_cm3=round(total_volume_cm3, 2),
            total_weight_kg=round(total_weight_kg, 2),
            references=resolved_references,
            boxes_used=boxes_used,
            missing_codes=missing_codes,
            notes=notes,
        )

    def _select_boxes(self, box_type: str | None) -> list[ShipmentBox]:
        if not box_type:
            return DEFAULT_BOXES

        filtered = [box for box in DEFAULT_BOXES if box.code.upper() == box_type.upper()]
        return filtered or DEFAULT_BOXES

    def _build_reference_response(
        self,
        reference: ReferenceRecord,
        quantity: int,
    ) -> ReferenceResolvedResponse:
        return ReferenceResolvedResponse(
            code=reference.code,
            name=reference.name,
            quantity=quantity,
            dimensions=DimensionResponse(
                length_cm=reference.dimensions.length_cm,
                width_cm=reference.dimensions.width_cm,
                height_cm=reference.dimensions.height_cm,
                volume_cm3=round(reference.dimensions.volume_cm3, 2),
            ),
            unit_weight_kg=reference.weight_kg,
            total_weight_kg=round(reference.weight_kg * quantity, 2),
        )

    def _build_box_response(self, bin_result: Bin, boxes: list[ShipmentBox]) -> BoxPlanResponse:
        box_lookup = {box.code: box for box in boxes}
        box = box_lookup[bin_result.name]
        fitted_items = [
            PackedItemResponse(
                code=item.name.split("__")[0],
                instance=item.name,
                position=self._to_float_list(getattr(item, "position", [0, 0, 0])),
                rotation_type=getattr(item, "rotation_type", None),
            )
            for item in bin_result.items
        ]
        unfitted_items = [item.name for item in getattr(bin_result, "unfitted_items", [])]
        total_weight_kg = sum(float(item.weight) for item in bin_result.items)

        return BoxPlanResponse(
            box_code=box.code,
            dimensions=DimensionResponse(
                length_cm=box.dimensions.length_cm,
                width_cm=box.dimensions.width_cm,
                height_cm=box.dimensions.height_cm,
                volume_cm3=round(box.dimensions.volume_cm3, 2),
            ),
            max_weight_kg=box.max_weight_kg,
            total_weight_kg=round(total_weight_kg, 2),
            fitted_items=fitted_items,
            unfitted_items=unfitted_items,
        )

    def _to_float_list(self, values: list[Decimal | float | int]) -> list[float]:
        return [float(value) for value in values]
