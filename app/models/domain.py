from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensions:
    length_cm: float
    width_cm: float
    height_cm: float

    @property
    def volume_cm3(self) -> float:
        return self.length_cm * self.width_cm * self.height_cm


@dataclass(frozen=True)
class ReferenceRecord:
    code: str
    name: str
    dimensions: Dimensions
    weight_kg: float


@dataclass(frozen=True)
class ShipmentBox:
    code: str
    dimensions: Dimensions
    max_weight_kg: float
