from enum import Enum

from pydantic import BaseModel, Field


class DataSourceType(str, Enum):
    mock = "mock"
    database = "database"
    google_sheet = "google_sheet"


class PackingRequestItem(BaseModel):
    code: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1)


class PackingRequest(BaseModel):
    source: DataSourceType = DataSourceType.mock
    items: list[PackingRequestItem] = Field(min_length=1)
    box_type: str | None = None
    notification_email: str | None = None


class DimensionResponse(BaseModel):
    length_cm: float
    width_cm: float
    height_cm: float
    volume_cm3: float


class ReferenceResolvedResponse(BaseModel):
    code: str
    name: str
    quantity: int
    dimensions: DimensionResponse
    unit_weight_kg: float
    total_weight_kg: float


class PackedItemResponse(BaseModel):
    code: str
    instance: str
    position: list[float]
    rotation_type: int | None = None


class BoxPlanResponse(BaseModel):
    box_code: str
    dimensions: DimensionResponse
    max_weight_kg: float
    total_weight_kg: float
    fitted_items: list[PackedItemResponse]
    unfitted_items: list[str]


class PackingResponse(BaseModel):
    source: DataSourceType
    total_requested_items: int
    total_volume_cm3: float
    total_weight_kg: float
    references: list[ReferenceResolvedResponse]
    boxes_used: list[BoxPlanResponse]
    missing_codes: list[str]
    notes: list[str]
