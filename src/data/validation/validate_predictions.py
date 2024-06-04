import numpy as np
import pandas as pd
from src.config import settings
import dagshub
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from src.serve.database import create_database_client


def main():
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    client = create_database_client()

    db = client.electricity_predictor

    for model_type in settings.prediction_subjects:
        mlflow.start_run(run_name=f"validate_predictions_{model_type}")

        collection = db[model_type + "_predictions"]
        all_documents = collection.find()
        document_count = collection.count_documents({})
        print("num of docs", document_count)

        latest_prediction_index = document_count - 1

        if model_type == "price":
            latest_prediction_index -= 1

        date = all_documents[latest_prediction_index]["date"]
        latest_document = all_documents[latest_prediction_index]
        print("latest document", latest_document)
        print(date)

        df = pd.read_csv(f"data/processed/{model_type}_data.csv")
        print(df.head())

        df['date'] = df['date'].str[:10]
        matching_rows = df[df['date'] == date]

        print(len(matching_rows))

        if model_type == "price":
            actual_values = matching_rows['price'].values.tolist()
        else:
            actual_values = matching_rows['production'].values.tolist()

        if len(actual_values) != len(latest_document['predictions']):
            print("Length of predictions does not match length of actual values")
            return

        errors = []
        for i in range(len(actual_values)):
            print(f"Prediction: {latest_document['predictions'][i]}, Actual: {actual_values[i]}")

            error = actual_values[i] - latest_document['predictions'][i]
            errors.append(error)

        mean_error = np.mean(errors)
        print(f"Mean error for price: {mean_error}")
        mean_squared_error = np.mean(np.square(errors))
        print(f"Mean squared error for price: {mean_squared_error}")

        mlflow.log_metric("mean_error", mean_error)
        mlflow.log_metric("mean_squared_error", mean_squared_error)
        mlflow.end_run()


if __name__ == "__main__":
    main()
