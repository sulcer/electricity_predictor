import os
from typing import Tuple
import joblib
import numpy as np
import pandas as pd
import tf2onnx
from keras import Sequential
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from src.config import settings
import onnxruntime as ort
from src.logger_config import logger
from mlflow.onnx import log_model as log_onnx_model
from mlflow.sklearn import log_model as log_sklearn_model


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

    # print(data.head())

    train_data, test_data = create_test_train_split(data)

    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    window_size = settings.window_size

    X_train, y_train = create_time_series(train_data, window_size)
    X_test, y_test = create_time_series(test_data, window_size)

    return X_train, y_train, X_test, y_test


def save_model(model: Sequential, scaler: MinMaxScaler, directory: str, X_test: np.array):
    client = MlflowClient()

    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, settings.window_size, (len(settings.features) + 1)), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    model_ = log_onnx_model(onnx_model=onnx_model,
                            artifact_path=f"models/{directory}",
                            signature=infer_signature(X_test, model.predict(X_test)),
                            registered_model_name="model_" + directory)

    mv = client.create_model_version(name="model_" + directory, source=model_.model_uri, run_id=model_.run_id)

    client.transition_model_version_stage("model_" + directory, mv.version, "staging")

    scaler_meta = {"feature_range": scaler.feature_range}
    scaler = log_sklearn_model(
        sk_model=scaler,
        artifact_path=f"scalers/{directory}",
        registered_model_name=directory + "_scaler",
        metadata=scaler_meta
    )

    sv = client.create_model_version(name=directory + "_scaler", source=scaler.model_uri, run_id=scaler.run_id)

    client.transition_model_version_stage(directory + "_scaler", sv.version, "staging")

    # if not os.path.exists(f"models/{directory}"):
    #     os.makedirs(f"models/{directory}")
    #
    # joblib.dump(scaler, f"models/{directory}/scaler.pkl")
    #
    # with open(f"models/{directory}/model.onnx", "wb") as f:
    #     f.write(onnx_model.SerializeToString())


def load_onnx_model(path: str) -> ort.InferenceSession:
    return ort.InferenceSession(path)


def load_scaler(path: str) -> MinMaxScaler:
    return joblib.load(path)


def evaluate_model(y_actual: np.array, predicted: np.array, scaler: MinMaxScaler) -> Tuple[float, float, float]:
    predicted_copy_array = np.repeat(predicted, (len(settings.features) + 1), axis=-1)
    pred = scaler.inverse_transform(
        np.reshape(predicted_copy_array, (len(predicted), (len(settings.features) + 1))))[:, 0]

    actual_copy_array = np.repeat(y_actual, (len(settings.features) + 1), axis=-1)
    actual = scaler.inverse_transform(
        np.reshape(actual_copy_array, (len(y_actual), (len(settings.features) + 1))))[:, 0]

    mse = mean_squared_error(actual, pred)
    mae = mean_absolute_error(actual, pred)
    evs = explained_variance_score(actual, pred)

    return mse, mae, evs


def write_evaluation_metrics_to_file(model_name: str, mse: float, mae: float, evs: float, file_path: str):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"Train MSE: {mse}\n")
        file.write(f"Train MAE: {mae}\n")
        file.write(f"Train EVS: {evs}\n")


def run_sklearn_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    if data.isnull().values.any():
        logger.warning("Missing data in row")
        numeric_features = data.select_dtypes(include=['int64', 'float64']).columns

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numeric_features)
            ])

        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor)
        ])

        transformed_data = pipeline.fit_transform(data)
        return transformed_data
