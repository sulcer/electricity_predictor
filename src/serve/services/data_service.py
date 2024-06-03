import pandas as pd


class DataService:
    def __init__(self):
        pass

    @staticmethod
    def get_price_data():
        # url = "https://dagshub.com/sulcer/electricity_predictor/raw/main/data/processed/price_data.csv"
        # df = pd.read_csv(url)
        df = pd.read_csv("data/processed/price_data.csv")
        df.drop('date', axis=1, inplace=True)

        return df
