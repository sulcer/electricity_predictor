import joblib
from sklearn.preprocessing import MinMaxScaler
from src.config import settings
from src.data.fetch import Fetcher
import onnxruntime as ort
from src.serve.helpers.common import create_time_series, use_model_prediction
from src.serve.services.data_service import DataService


class MLService:
    def __init__(self):
        self.window_size = settings.window_size

    def predict(self, model_type: str, n_time_units: int):
        fetcher = Fetcher()
        forcast = fetcher.fetch_weather_forcast()

        model = ort.InferenceSession(f"models/{model_type}/model_production.onnx")
        scaler: MinMaxScaler = joblib.load(f"models/{model_type}/scaler_production.gz")

        data_service = DataService()
        dataset = data_service.get_data(model_type)

        predictions = []
        last_rows = dataset.tail(self.window_size).values.tolist()
        feature_cols = list(range(len(last_rows[0])))

        for n in range(n_time_units):
            scaled_data = scaler.transform(last_rows)

            X = create_time_series(scaled_data, self.window_size, feature_cols)
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

        return predictions
