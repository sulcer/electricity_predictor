import os
from enum import auto, Enum
import dagshub
import joblib
import onnx
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from mlflow import MlflowClient
from src.config import settings
from mlflow.onnx import load_model as load_onnx
from mlflow.sklearn import load_model as load_scaler

from src.logger_config import logger


def get_latest_model(prediction_subject: str):
    try:
        client = MlflowClient()
        model_version = client.get_latest_versions("model_" + prediction_subject, stages=["staging"])[0]
        model_url = model_version.source
        model = load_onnx(model_url)
        return model
    except IndexError:
        print(f"Model for {prediction_subject} not found.")
        return None


def get_latest_scaler(prediction_subject: str):
    try:
        client = MlflowClient()
        model_version = (
            client.get_latest_versions(prediction_subject + "_scaler", stages=["staging"]))[0]
        model_url = model_version.source
        scaler = load_scaler(model_url)
        return scaler
    except IndexError:
        print(f"Scaler for {prediction_subject} not found.")
        return None


def get_production_model(prediction_subject: str):
    try:
        client = MlflowClient()
        model_version = client.get_latest_versions("model_" + prediction_subject, stages=["production"])[0]
        model_url = model_version.source
        model = load_onnx(model_url)
        return model
    except IndexError:
        print(f"Production model for {prediction_subject} not found.")
        return None


def get_production_scaler(prediction_subject: str):
    try:
        client = MlflowClient()
        model_version = (
            client.get_latest_versions(prediction_subject + "_scaler", stages=["production"]))[0]
        model_url = model_version.source
        scaler = load_scaler(model_url)
        return scaler
    except IndexError:
        print(f"Production scaler for {prediction_subject} not found.")
        return None


class ModelType(Enum):
    LATEST = auto()
    PRODUCTION = auto()


def download_model(prediction_subject: str, model_type: ModelType) -> tuple:
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    model_func = get_latest_model if model_type == ModelType.LATEST else get_production_model
    scaler_func = get_latest_scaler if model_type == ModelType.LATEST else get_production_scaler

    model = model_func(prediction_subject)
    scaler = scaler_func(prediction_subject)

    folder_name = f"models/{prediction_subject}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if model is None or scaler is None:
        return None, None

    model_type_str = model_type.name.lower()
    joblib.dump(scaler, f"{folder_name}/scaler_{model_type_str}.gz")
    onnx.save_model(model, f"{folder_name}/model_{model_type_str}.onnx")

    model_path = f"{folder_name}/model_{model_type_str}.onnx"

    return model_path, scaler


def download_model_registry():
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    for prediction_subject in settings.prediction_subjects:
        model_path = f"models/{prediction_subject}/model_production.onnx"
        scaler_path = f"models/{prediction_subject}/scaler_production.gz"

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            logger.info(f"Model and scaler for {prediction_subject} already exist.")
            continue

        model = get_production_model(prediction_subject)
        scaler = get_production_scaler(prediction_subject)

        if not os.path.exists(f"models/{prediction_subject}"):
            os.makedirs(f"models/{prediction_subject}")

        joblib.dump(scaler, f"models/{prediction_subject}/scaler_production.gz")
        onnx.save_model(model, f"models/{prediction_subject}/model_production.onnx")

        logger.info(f"Model and scaler for {prediction_subject} downloaded.")


def empty_model_registry():
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    client = MlflowClient()
    for prediction_subject in settings.prediction_subjects:
        try:
            client.delete_registered_model(f"model_{prediction_subject}")
            client.delete_registered_model(f"{prediction_subject}_scaler")
        except IndexError:
            print(f"Model and scaler for {prediction_subject} not found.")
            continue
