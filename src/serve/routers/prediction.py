import joblib
from fastapi import APIRouter, HTTPException
import onnxruntime as ort
from sklearn.preprocessing import MinMaxScaler

from src.config import settings
from src.data.fetch import Fetcher
from src.serve.helpers.common import create_time_series, use_model_prediction, get_model_types
from src.serve.services.data_service import DataService

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)

window_size = settings.window_size


@router.get("/predict/{model_type}/{n_time_units}")
def predict(model_type: str, n_time_units: int):
    if model_type not in get_model_types():
        raise HTTPException(status_code=400, detail=f"Model type {model_type} not found")

    if n_time_units < 1 or n_time_units > 24:
        raise HTTPException(status_code=400, detail=f"Number of future time units must be between 1 and 24")

    fetcher = Fetcher()
    forcast = fetcher.fetch_weather_forcast()

    model = ort.InferenceSession(f"models/{model_type}/model.onnx")
    scaler: MinMaxScaler = joblib.load(f"models/{model_type}/scaler.pkl")

    data_service = DataService()
    dataset = data_service.get_data(model_type)

    print(forcast)

    predictions = []
    last_rows = dataset.tail(window_size).values.tolist()
    feature_cols = list(range(len(last_rows[0])))

    for n in range(n_time_units):
        scaled_data = scaler.transform(last_rows)

        X = create_time_series(scaled_data, window_size, feature_cols)
        prediction = use_model_prediction(X, model, scaler, feature_cols)
        predictions.append(prediction)

        new_row = [prediction,
                   forcast["temperature_2m"][n],
                   forcast["relative_humidity_2m"][n],
                   forcast["precipitation"][n],
                   forcast["cloud_cover"][n],
                   forcast["wind_speed_10m"][n]]

        print(new_row)
        last_rows.pop(0)
        last_rows.append(new_row)

    return {"message": predictions}
