import joblib
import pandas as pd
import tensorflow as tf
import tf2onnx
from sklearn.preprocessing import MinMaxScaler
from src.config import settings
from src.models.helpers.price_prediction.model import train_model
from src.models.helpers.price_prediction.preprocessing import preprocess_data


def run_model():
    data = pd.read_csv("data/processed/price_data.csv")
    scaler = MinMaxScaler()

    X_train, y_train, X_test, y_test = preprocess_data(data, scaler)

    model = train_model(X_train, y_train, X_test, y_test)

    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, settings.window_size, (len(settings.features) + 1)), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    joblib.dump(scaler, f"models/scaler/minmax.pkl")

    with open(f"models/model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())

    print("Training model finished")


if __name__ == "__main__":
    run_model()
