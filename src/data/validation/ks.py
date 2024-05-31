import numpy as np
import pandas as pd


def ks_test(sample1, sample2):
    if np.array_equal(sample1, sample2):
        # If the samples are equal, return trivial values x
        return 0.0, 1.0
    else:
        # Calculate the cumulative distribution functions
        hist1, bin_edges1 = np.histogram(sample1, bins=100, density=True)
        hist2, bin_edges2 = np.histogram(sample2, bins=100, density=True)
        cdf1 = np.cumsum(hist1 * np.diff(bin_edges1))
        cdf2 = np.cumsum(hist2 * np.diff(bin_edges2))
        d = np.max(np.abs(cdf1 - cdf2))
        # Calculate the p-value using an approximation
        p_value = 1.0 - np.exp(-2 * (d ** 2))
        return d, p_value


if __name__ == "__main__":
    current_data = pd.read_csv("data/processed/current_data.csv")
    reference_data = pd.read_csv("data/processed/reference_data.csv")

    alpha = 0.1

    for column in current_data.columns:
        d, p_value = ks_test(current_data[column], reference_data[column])
        if p_value < alpha:
            print(f"Data drift detected in column {column} with p-value {p_value}")
        else:
            print(f"No data drift detected in column {column} with p-value {p_value}")
