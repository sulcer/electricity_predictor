from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from src.config import settings
from src.models.helpers.common import create_test_train_split, create_time_series


def preprocess_data(data: pd.DataFrame, scaler: MinMaxScaler) -> Tuple[np.array, np.array, np.array, np.array]:
    data.drop('date', axis=1, inplace=True)

    print(data.head())

    train_data, test_data = create_test_train_split(data)

    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    window_size = settings.window_size

    X_train, y_train = create_time_series(train_data, window_size)
    X_test, y_test = create_time_series(test_data, window_size)

    return X_train, y_train, X_test, y_test
