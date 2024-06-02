import os
import pandas as pd
from src.logger_config import logger
from src.models.helpers.common import preprocess_data, load_onnx_model, load_scaler, evaluate_model, \
    write_evaluation_metrics_to_file


def predict_model():
    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            prediction_subject = file.replace("_data.csv", "")
            logger.info(f"Running model training for {prediction_subject}")

            data = pd.read_csv(f"data/processed/{file}")

            model = load_onnx_model(f"models/{prediction_subject}/model.onnx")
            scaler = load_scaler(f"models/{prediction_subject}/scaler.pkl")

            _, _, X_test, y_test = preprocess_data(data, scaler)

            input_names = model.get_inputs()[0].name
            output_names = model.get_outputs()[0].name

            predictions = model.run([output_names], {input_names: X_test})[0]

            mse_latest, mae_latest, evs_latest = evaluate_model(y_test, predictions, scaler)

            print(f'MSE: {mse_latest:.2f}')
            print(f'MAE: {mae_latest:.2f}')
            print(f'EVS: {evs_latest:.2f}')

            write_evaluation_metrics_to_file("GRU", mse_latest, mae_latest, evs_latest,
                                             f"reports/{prediction_subject}/latest_metrics.txt")


if __name__ == "__main__":
    predict_model()
