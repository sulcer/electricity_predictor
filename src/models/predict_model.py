import os
import pandas as pd
from src.logger_config import logger
from src.models.helpers.common import preprocess_data, load_onnx_model, load_scaler, evaluate_model, \
    write_evaluation_metrics_to_file
import dagshub
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from mlflow import MlflowClient
from src.config import settings


def predict_model():
    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            prediction_subject = file.replace("_data.csv", "")
            logger.info(f"Running model prediction for {prediction_subject}")

            mlflow.start_run(run_name=f"train_{prediction_subject}_model")

            data = pd.read_csv(f"data/processed/{file}")

            model = load_onnx_model(f"models/{prediction_subject}/model.onnx")
            scaler = load_scaler(f"models/{prediction_subject}/scaler.pkl")

            _, _, X_test, y_test = preprocess_data(data, scaler)

            input_names = model.get_inputs()[0].name
            output_names = model.get_outputs()[0].name

            predictions = model.run([output_names], {input_names: X_test})[0]

            mse_latest, mae_latest, evs_latest = evaluate_model(y_test, predictions, scaler)

            mlflow.log_metric("MSE", mse_latest)
            mlflow.log_metric("MAE", mae_latest)
            mlflow.log_metric("EVS", evs_latest)

            write_evaluation_metrics_to_file("GRU", mse_latest, mae_latest, evs_latest,
                                             f"reports/{prediction_subject}/latest_metrics.txt")

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
