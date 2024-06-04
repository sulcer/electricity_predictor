import numpy as np
import tf_keras
from keras import Sequential, Input
from keras.src.layers import GRU, Dropout, Dense
from keras.src.optimizers import Adam
import tensorflow_model_optimization as tfmot
from tensorflow_model_optimization.python.core.quantization.keras.default_8bit import default_8bit_quantize_scheme
from src.config import settings
from dagshub.data_engine.datasources import mlflow


def build_model(input_shape: np.array) -> Sequential:
    model = Sequential(name='GRU')
    optimizer = Adam(learning_rate=0.01)

    model.add(Input(shape=(input_shape.shape[1], input_shape.shape[2])))
    model.add(GRU(128, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(64, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(32))
    model.add(Dense(units=32, activation="relu"))
    model.add(Dense(1))

    model.compile(optimizer=optimizer, loss="mean_squared_error")
    return model


def build_quantized_model(input_shape: np.array) -> Sequential:
    quantize_annotate_layer = tfmot.quantization.keras.quantize_annotate_layer

    model = tf_keras.Sequential(name="GRU")
    model.add(tf_keras.Input(shape=(input_shape.shape[1], input_shape.shape[2])))
    model.add(tf_keras.layers.GRU(units=128, return_sequences=True))
    model.add(tf_keras.layers.Dropout(0.2))
    model.add(tf_keras.layers.GRU(units=64, return_sequences=True))
    model.add(tf_keras.layers.Dropout(0.2))
    model.add(tf_keras.layers.GRU(units=32))
    model.add(quantize_annotate_layer(tf_keras.layers.Dense(units=32, activation="relu")))
    model.add(quantize_annotate_layer(tf_keras.layers.Dense(units=1)))

    optimizer = tf_keras.optimizers.legacy.Adam(learning_rate=0.01)

    model = tfmot.quantization.keras.quantize_apply(
        model,
        scheme=default_8bit_quantize_scheme.Default8BitQuantizeScheme(),
        quantized_layer_name_prefix='quant_'
    )

    model.compile(optimizer=optimizer, loss="mean_squared_logarithmic_error")

    return model


def train_model(X_train: np.array, y_train: np.array, X_test: np.array, y_test: np.array) -> Sequential:
    epochs = 10
    batch_size = 64
    window_size = settings.window_size

    model = build_quantized_model(X_train)

    model.fit(X_train, y_train,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(X_test, y_test),
              verbose=1)

    mlflow.log_param("window_size", window_size)
    mlflow.log_param("batch_size", batch_size)
    mlflow.log_param("epochs", epochs)

    return model
