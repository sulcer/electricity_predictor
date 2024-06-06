from fastapi import APIRouter
from src.serve.services.experiments_service import ExperimentService

router = APIRouter(
    tags=["experiments"],
    prefix="/experiments"
)


@router.get(
    "/validate_predictions",
    summary="Get Validate Predictions experiments",
    description="Fetches the validate predictions experiments.",
    response_description="The validate predictions experiments."
)
def get_validate_predictions_experiments():
    experiments_service = ExperimentService()
    data = experiments_service.get_validate_predictions_experiments()

    return data


@router.get(
    "/train_model",
    summary="Get Train Model experiments",
    description="Fetches the train model experiments.",
    response_description="The train model experiments."
)
def get_train_model_experiments():
    experiments_service = ExperimentService()
    data = experiments_service.get_train_model_experiments()

    return data
