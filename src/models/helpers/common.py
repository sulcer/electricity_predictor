import os
from typing import Tuple
import joblib
import numpy as np
import pandas as pd
import tf2onnx
from keras import Sequential
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from src.config import settings


def create_test_train_split(dataset: pd.DataFrame, split_size=0.1) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_data_size = round(split_size * len(dataset))
    train_data = dataset[:-test_data_size]
    test_data = dataset[-test_data_size:]

    return train_data, test_data


def create_time_series(data: pd.DataFrame, n_past: int) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(n_past, len(data)):
        X.append(data[i - n_past:i, 0:data.shape[1]])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def preprocess_data(data: pd.DataFrame, scaler: MinMaxScaler) -> Tuple[np.array, np.array, np.array, np.array]:
    data.drop('date', axis=1, inplace=True)

    print(data.head())

    train_data, test_data = create_test_train_split(data)

    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    window_size = settings.window_size

    X_train, y_train = create_time_series(train_data, window_size)
    X_test, y_test = create_time_series(test_data, window_size)

    return X_train, y_train, X_test, y_test


def save_model(model: Sequential, scaler: MinMaxScaler, directory: str):
    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, settings.window_size, (len(settings.features) + 1)), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    if not os.path.exists(f"models/{directory}"):
        os.makedirs(f"models/{directory}")

    joblib.dump(scaler, f"models/{directory}/minmax.pkl")

    with open(f"models/{directory}/model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())
