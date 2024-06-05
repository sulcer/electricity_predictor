from fastapi import APIRouter
from src.serve.services.data_service import DataService

router = APIRouter(
    tags=["price"],
    prefix="/price"
)


@router.get(
    "",
    summary="Get Latest Price Data",
    description="Fetches the latest price data.",
    response_description="The latest price data."
)
def get_latest_price_data():
    data_service = DataService()
    data = data_service.get_latest_data('price')

    return data
