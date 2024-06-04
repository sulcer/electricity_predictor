import os
import pandas as pd
from mlflow import MlflowClient
from src.logger_config import logger
from src.models.helpers.common import preprocess_data, evaluate_model, \
    write_evaluation_metrics_to_file
import dagshub
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from src.config import settings
from src.models.model_registry import download_model, ModelType
import onnxruntime as ort


def set_production_model(prediction_subject: str) -> None:
    client = MlflowClient()

    try:
        new_model_version = (
            client.get_latest_versions("model_" + prediction_subject, stages=["staging"])[0])
        new_scaler_version = (
            client.get_latest_versions(prediction_subject + "_scaler", stages=["staging"])[0])

        client.transition_model_version_stage("model_" + prediction_subject,
                                              new_model_version.version,
                                              "production")
        client.transition_model_version_stage(prediction_subject + "_scaler",
                                              new_scaler_version.version,
                                              "production")

        logger.info(f"Model and scaler for {prediction_subject} set to production")
    except IndexError:
        logger.error(f"Model for {prediction_subject} not found.")


def predict_model():
    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            prediction_subject = file.replace("_data.csv", "")
            logger.info(f"Running model prediction for {prediction_subject}")

            mlflow.start_run(run_name=f"train_{prediction_subject}_model", nested=True)

            production_model_path, production_scaler = download_model(prediction_subject, ModelType.PRODUCTION)
            latest_model_path, scaler = download_model(prediction_subject, ModelType.LATEST)

            if latest_model_path is None and scaler is None:
                return

            if production_model_path is None and production_scaler is None:
                set_production_model(prediction_subject)
                return

            latest_model = ort.InferenceSession(latest_model_path)
            production_model = ort.InferenceSession(production_model_path)

            data = pd.read_csv(f"data/processed/{file}")

            _, _, X_test, y_test = preprocess_data(data, scaler)

            input_names = latest_model.get_inputs()[0].name
            output_names = latest_model.get_outputs()[0].name

            latest_model_predictions = latest_model.run([output_names], {input_names: X_test})[0]

            mse_latest, mae_latest, evs_latest = evaluate_model(y_test, latest_model_predictions, scaler)

            mlflow.log_metric("MSE_latest", mse_latest)
            mlflow.log_metric("MAE_latest", mae_latest)
            mlflow.log_metric("EVS_latest", evs_latest)

            input_names = production_model.get_inputs()[0].name
            output_names = production_model.get_outputs()[0].name

            production_model_predictions = production_model.run([output_names], {input_names: X_test})[0]

            mse_production, mae_production, evs_production = (
                evaluate_model(y_test, production_model_predictions, scaler))

            if mse_latest < mse_production:
                set_production_model(prediction_subject)

            if not os.path.exists(f"reports/{prediction_subject}"):
                os.makedirs(f"reports/{prediction_subject}")

            write_evaluation_metrics_to_file("GRU", mse_latest, mae_latest, evs_latest,
                                             f"reports/{prediction_subject}/latest_metrics.txt")

            write_evaluation_metrics_to_file("GRU", mse_production, mae_production, evs_production,
                                             f"reports/{prediction_subject}/production_metrics.txt")

            logger.info(f"Predicting for model {prediction_subject} finished")
            mlflow.end_run()

    logger.info("Prediction finished")


if __name__ == "__main__":
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    if mlflow.active_run():
        mlflow.end_run()

    predict_model()
