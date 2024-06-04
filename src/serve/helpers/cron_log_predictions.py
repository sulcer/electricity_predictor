from datetime import datetime
from src.config import settings
from src.serve.services.ml_service import MLService


def save_daliy_predictions(client):
    ml_service = MLService()

    db = client.electricity_predictor

    for model_type in settings.prediction_subjects:
        print(model_type)
        predictions = ml_service.predict(model_type, 24)

        collection = db[model_type + "_predictions"]

        collection.insert_one({"predictions": predictions, 'date': datetime.now().strftime("%Y-%m-%d")})
