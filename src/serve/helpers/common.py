import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def create_time_series(data: pd.DataFrame, window_size: int, feature_cols: list) -> np.ndarray:
    sequences = []
    n_samples = len(data)

    for i in range(window_size, n_samples + 1):
        sequence = data[i - window_size:i, feature_cols]
        sequences.append(sequence)

    return np.array(sequences)


def use_model_prediction(data: np.array, model, scaler: MinMaxScaler, feature_cols: list) -> float:
    prediction = model.run(["output"], {"input": data})[0]

    prediction_copies_array = np.repeat(prediction, len(feature_cols), axis=-1)
    prediction_reshaped = np.reshape(prediction_copies_array, (len(prediction), len(feature_cols)))
    prediction = scaler.inverse_transform(prediction_reshaped)[:, 0]

    return float("{0:.2f}".format(prediction.tolist()[0]))


def get_model_types():
    model_types = ['price',
                   'production_cross',
                   'production_fossil',
                   'production_hydro',
                   'production_nuclear']

    return model_types
