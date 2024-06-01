import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from src.config import settings
from src.models.helpers.common import preprocess_data, load_onnx_model, load_scaler


def predict_model():
    data = pd.read_csv("data/processed/price_data.csv")

    model = load_onnx_model("models/price/model.onnx")
    scaler = load_scaler("models/price/scaler.pkl")

    _, _, X_test, y_test = preprocess_data(data, scaler)

    input_names = model.get_inputs()[0].name
    output_names = model.get_outputs()[0].name

    predicted = model.run([output_names], {input_names: X_test})[0]

    predicted_copy_array = np.repeat(predicted, (len(settings.features) + 1), axis=-1)

    pred = scaler.inverse_transform(
        np.reshape(predicted_copy_array, (len(predicted), (len(settings.features) + 1))))[:, 0]
    actual_copy_array = np.repeat(y_test, (len(settings.features) + 1), axis=-1)
    actual = scaler.inverse_transform(
        np.reshape(actual_copy_array, (len(y_test), (len(settings.features) + 1))))[:, 0]

    mse = mean_squared_error(actual, pred)
    mae = mean_absolute_error(actual, pred)
    evs = explained_variance_score(actual, pred)

    print(f'MSE: {mse:.2f}')
    print(f'MAE: {mae:.2f}')
    print(f'EVS: {evs:.2f}')


if __name__ == "__main__":
    predict_model()
