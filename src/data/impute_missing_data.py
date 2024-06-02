import numpy as np
import pandas as pd


def impute():
    # df = pd.read_csv("../../data/processed/production_nuclear_data.csv")
    #
    # # Check for missing values
    # missing_values = df.isnull().sum()
    # print(missing_values)
    # print(df.head())
    #
    # # Select only the numerical columns
    # numerical_columns = df.select_dtypes(include=[np.number]).columns
    #
    # # Impute missing values with the mean
    # df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())
    #
    # # Check for missing values
    # missing_values = df.isnull().sum()
    # print(missing_values)
    # print(df.head())
    #
    # # save the imputed data
    # df.to_csv("../../data/processed/production_nuclear_data.csv", index=False)

    data = {
        'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
        'A': [1, 2, np.nan, 4, 5],
        'B': [np.nan, 1, 2, np.nan, 5],
        'C': [1, 2, 3, 4, 5]
    }
    df = pd.DataFrame(data)

    print(df.isnull().values.any())


if __name__ == "__main__":
    impute()
