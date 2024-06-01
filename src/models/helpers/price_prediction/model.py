import numpy as np
from keras import Sequential, Input
from keras.src.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.src.layers import Bidirectional, GRU, Dropout, Dense
from keras.src.optimizers import Adam


def build_model(input_shape: np.array) -> Sequential:
    model = Sequential(name='Bidirectional_GRU')
    optimizer = Adam(learning_rate=0.001)

    model.add(Input(shape=(input_shape.shape[1], input_shape.shape[2])))
    model.add(Bidirectional(GRU(128, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(GRU(64, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(GRU(32)))
    model.add(Dense(units=32, activation="relu"))
    model.add(Dense(1))

    model.compile(optimizer=optimizer, loss="mean_squared_error")
    return model


def train_model(X_train: np.array, y_train: np.array, X_test: np.array, y_test: np.array) -> Sequential:
    epochs = 50
    batch_size = 64

    model = build_model(X_train)

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)

    model.fit(X_train, y_train,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(X_test, y_test),
              verbose=1,
              callbacks=[early_stopping, reduce_lr])

    return model
