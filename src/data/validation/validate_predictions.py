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
    collection = db.price_predictions

    all_documents = collection.find()

    for document in all_documents:
        print(document)


if __name__ == "__main__":
    main()
