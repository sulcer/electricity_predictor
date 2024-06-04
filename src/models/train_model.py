import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.logger_config import logger
from src.models.helpers.common import preprocess_data, save_model, run_sklearn_pipeline
from src.models.helpers.price_prediction import price_model
from src.models.helpers.production_prediction import production_model
import dagshub
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from src.config import settings


def run_model():
    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            train_subject = file.replace("_data.csv", "")
            logger.info(f"Running model training for {train_subject}")

            mlflow.start_run(run_name=f"train_{train_subject}_model")

            data = pd.read_csv(f"data/processed/{file}")

            run_sklearn_pipeline(data)

            scaler = MinMaxScaler()

            print(data.isnull().sum())

            X_train, y_train, X_test, y_test = preprocess_data(data, scaler)

            if train_subject == 'price':
                model = price_model(X_train, y_train, X_test, y_test)
                save_model(model, scaler, train_subject, X_test)
            elif 'production' in train_subject:
                model = production_model(X_train, y_train, X_test, y_test)
                save_model(model, scaler, train_subject, X_test)

            logger.info(f"Model for {train_subject} trained")
            mlflow.end_run()

    logger.info("Training finished")


if __name__ == "__main__":
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    if mlflow.active_run():
        mlflow.end_run()

    run_model()
