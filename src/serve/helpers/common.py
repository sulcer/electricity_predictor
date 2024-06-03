import numpy as np


def create_time_series(data, window_size, feature_cols):
    sequences = []
    n_samples = len(data)

    for i in range(window_size, n_samples + 1):
        sequence = data[i - window_size:i, feature_cols]
        sequences.append(sequence)

    return np.array(sequences)


def use_model_prediction(data, model, scaler, feature_cols):
    prediction = model.run(["output"], {"input": data})[0]

    prediction_copies_array = np.repeat(prediction, len(feature_cols), axis=-1)
    prediction_reshaped = np.reshape(prediction_copies_array, (len(prediction), len(feature_cols)))
    prediction = scaler.inverse_transform(prediction_reshaped)[:, 0]

    return int(prediction.tolist()[0])