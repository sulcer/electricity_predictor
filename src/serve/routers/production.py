from fastapi import HTTPException
from fastapi import APIRouter
from src.config import settings
from src.serve.services.data_service import DataService

router = APIRouter(
    tags=["production"],
    prefix="/production"
)

types = settings.production_types


@router.get(
    "/{production_type}",
    summary="Get Latest Production Data",
    description="Fetches the latest production data for valid production types (cross, fossil, hydro, nuclear).",
    response_description="The latest production data for the specified type."
)
def get_latest_production_data(production_type: str):
    if production_type not in types:
        raise HTTPException(status_code=400, detail=f"Production type {production_type} not found")

    data_service = DataService()
    data = data_service.get_latest_data("production_" + production_type)

    return data
