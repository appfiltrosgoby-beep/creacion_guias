from fastapi import APIRouter

from app.schemas.reference import PackingRequest, PackingResponse
from app.services.packing_service import PackingService

router = APIRouter(prefix="/references", tags=["references"])
packing_service = PackingService()


@router.post("/optimize", response_model=PackingResponse)
def optimize_references(request: PackingRequest) -> PackingResponse:
    return packing_service.optimize(request)
