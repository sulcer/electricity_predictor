from fastapi import APIRouter, HTTPException
from src.serve.helpers.common import get_model_types
from src.serve.services.ml_service import MLService

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)


@router.get("/{model_type}/{n_time_units}")
def predict(model_type: str, n_time_units: int):
    if model_type not in get_model_types():
        raise HTTPException(status_code=400, detail=f"Model type {model_type} not found")

    if n_time_units < 1 or n_time_units > 24:
        raise HTTPException(
            status_code=400,
            detail=f"Number of future time units must be between 1 and 24. Got {n_time_units}")

    ml_service = MLService()
    predictions = ml_service.predict(model_type, n_time_units)

    return {"message": predictions}
