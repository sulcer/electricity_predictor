from datetime import datetime

import pandas as pd
import requests


class DataService:
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.price_url = f'https://api.energy-charts.info/price?bzn=SI&end={self.date}'
        self.production_url = f'https://api.energy-charts.info/public_power?country=si&start={self.date}'

    @staticmethod
    def get_data(data_type: str):
        # url = f"https://dagshub.com/sulcer/electricity_predictor/raw/main/data/processed/{data_type}_data.csv"
        # df = pd.read_csv(url)
        df = pd.read_csv(f"data/processed/{data_type}_data.csv")
        df.drop('date', axis=1, inplace=True)

        return df

    def get_latest_data(self, data_type: str):
        if data_type == 'price':
            url = self.price_url
        elif 'production' in data_type:
            url = self.production_url
        else:
            raise ValueError("Invalid data type")

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data_type == 'price':
            df = self.process_price_data(data)
        else:
            df = self.process_production_data(data, data_type)

        return df.values.tolist()

    @staticmethod
    def process_price_data(data):
        daily_price_data = []
        for i in range(len(data['price'])):
            timestamp = data['unix_seconds'][i]
            price = data['price'][i]

            new_data = {'date': timestamp, 'price': price}
            daily_price_data.append(new_data)

        df = pd.DataFrame(daily_price_data)

        return df

    @staticmethod
    def process_production_data(data, production_type: str):
        match production_type:
            case 'production_cross':
                production_type = 'Cross border electricity trading'
            case 'production_fossil':
                production_type = 'Fossil brown coal / lignite'
            case 'production_hydro':
                production_type = 'Hydro Run-of-River'
            case 'production_nuclear':
                production_type = 'Nuclear'
            case _:
                raise ValueError("Invalid production type")

        daily_production_data = []
        for i in range(len(data['production_types'])):
            if data['production_types'][i]['name'] == production_type:
                for j in range(len(data['production_types'][i]['data'])):
                    timestamp = data['unix_seconds'][j]
                    production = data['production_types'][i]['data'][j]

                    new_data = {'date': timestamp, 'production': production}
                    daily_production_data.append(new_data)
                break

        df = pd.DataFrame(daily_production_data)

        return df
