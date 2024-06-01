import numpy as np
from keras import Sequential, Input
from keras.src.layers import GRU, Dropout, Dense
from keras.src.optimizers import Adam


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


def train_model(X_train: np.array, y_train: np.array, X_test: np.array, y_test: np.array) -> Sequential:
    epochs = 10
    batch_size = 64

    model = build_model(X_train)

    model.fit(X_train, y_train,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(X_test, y_test),
              verbose=1)

    return model
