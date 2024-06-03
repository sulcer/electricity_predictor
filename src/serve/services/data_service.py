import pandas as pd


class DataService:
    def __init__(self):
        pass

    @staticmethod
    def get_data(data_type: str):
        # url = f"https://dagshub.com/sulcer/electricity_predictor/raw/main/data/processed/{data_type}_data.csv"
        # df = pd.read_csv(url)
        df = pd.read_csv(f"data/processed/{data_type}_data.csv")
        df.drop('date', axis=1, inplace=True)

        return df
