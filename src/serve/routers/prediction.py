import joblib
from fastapi import APIRouter
import onnxruntime as ort
from sklearn.preprocessing import MinMaxScaler

from src.config import settings
from src.data.fetch import Fetcher
from src.serve.helpers.common import create_time_series, use_model_prediction
from src.serve.services.data_service import DataService

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)

window_size = settings.window_size


@router.get("/predict/{model_type}/{n_time_units}")
def predict(model_type: str, n_time_units: int):
    fetcher = Fetcher()
    forcast = fetcher.fetch_weather_forcast()

    model = ort.InferenceSession(f"models/price/model.onnx")
    scaler: MinMaxScaler = joblib.load(f"models/price/scaler.pkl")

    data_service = DataService()
    dataset = data_service.get_price_data()

    print(forcast)

    predictions = []
    last_rows = dataset.tail(window_size).values.tolist()
    feature_cols = list(range(len(last_rows[0])))

    for n in range(n_time_units):
        scaled_data = scaler.transform(last_rows)

        X = create_time_series(scaled_data, window_size, feature_cols)
        prediction = use_model_prediction(X, model, scaler, feature_cols)
        predictions.append(prediction)

        forcast_index = n + 1

        new_row = [prediction,
                   forcast["temperature_2m"][forcast_index],
                   forcast["relative_humidity_2m"][forcast_index],
                   forcast["precipitation"][forcast_index],
                   forcast["cloud_cover"][forcast_index],
                   forcast["wind_speed_10m"][forcast_index]]

        print(new_row)
        last_rows.pop(0)
        last_rows.append(new_row)

    return {"message": predictions}
