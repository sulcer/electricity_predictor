import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.logger_config import logger
from src.models.helpers.common import preprocess_data, save_model
from src.models.helpers.price_prediction import price_model
from src.models.helpers.production_prediction import production_model


def run_model():
    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            train_subject = file.split('_')
            directory = file.replace("_data.csv", "")
            logger.info(f"Running model training for {directory}")

            data = pd.read_csv(f"data/processed/{file}")
            scaler = MinMaxScaler()

            X_train, y_train, X_test, y_test = preprocess_data(data, scaler)

            if train_subject == 'price':
                model = price_model(X_train, y_train, X_test, y_test)
                save_model(model, scaler, directory)
            elif train_subject == 'production':
                model = production_model(X_train, y_train, X_test, y_test)
                save_model(model, scaler, directory)

    logger.info("Training models finished")


if __name__ == "__main__":
    run_model()
