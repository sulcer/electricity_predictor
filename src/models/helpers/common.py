from typing import Tuple
import numpy as np
import pandas as pd


def create_test_train_split(dataset: pd.DataFrame, split_size=0.1) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_data_size = round(split_size * len(dataset))
    train_data = dataset[:-test_data_size]
    test_data = dataset[-test_data_size:]

    return train_data, test_data


def create_time_series(data: pd.DataFrame, n_past: int) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(n_past, len(data)):
        X.append(data[i - n_past:i, 0:data.shape[1]])
        y.append(data[i, 0])
    return np.array(X), np.array(y)
