import os
import numpy as np
import pandas as pd
from src.logger_config import logger


def ks_test(sample1, sample2):
    if np.array_equal(sample1, sample2):
        return 0.0, 1.0
    else:
        hist1, bin_edges1 = np.histogram(sample1, bins=100, density=True)
        hist2, bin_edges2 = np.histogram(sample2, bins=100, density=True)
        cdf1 = np.cumsum(hist1 * np.diff(bin_edges1))
        cdf2 = np.cumsum(hist2 * np.diff(bin_edges2))
        d = np.max(np.abs(cdf1 - cdf2))
        p_value = 1.0 - np.exp(-2 * (d ** 2))
        return d, p_value


def impute_missing_values(df):
    df.drop(columns=["date"], inplace=True)
    return df.apply(lambda x: x.fillna(x.median()), axis=0)


if __name__ == "__main__":
    alpha = 0.1

    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            tests_subject = file.replace(".csv", "")

            logger.info(f"Running Kolmogorov Smirnov test for {tests_subject}")

            current_data = pd.read_csv(f"data/processed/{file}")
            reference_data = pd.read_csv(f"data/processed/reference_{file}")

            current_data = impute_missing_values(current_data)
            reference_data = impute_missing_values(reference_data)

            for column in current_data.columns:
                d, p_value = ks_test(current_data[column], reference_data[column])
                if p_value < alpha:
                    logger.warning(f"Data drift detected in column {column} with p-value {p_value}")
                else:
                    logger.info(f"No data drift detected in column {column} with p-value {p_value}")
