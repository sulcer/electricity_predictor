import os
from datetime import datetime, timedelta
import pandas as pd
import requests


class Fetcher:
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.price_url = f'https://api.energy-charts.info/price?bzn=SI&end={self.date}'
        self.production_url = \
            f'https://api.energy-charts.info/public_power?country=si&start={self.past_date}&end={self.past_date}'
        self.weather_url = ("https://api.open-meteo.com/v1/forecast?latitude=46.0833&longitude=15&hourly"
                            "=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,cloud_cover,"
                            "wind_speed_10m&timezone=Europe%2FBerlin&forecast_days=1")
        self.data_path = "data"

    def fetch_price_data(self):
        response = requests.get(self.price_url)
        response.raise_for_status()
        data = response.json()

        daily_price_data = []
        for i in range(len(data['price'])):
            timestamp = datetime.fromtimestamp(data['unix_seconds'][i]).strftime('%Y-%m-%dT%H:%M:%S')
            price = data['price'][i]

            new_data = {'date': timestamp, 'price': price}
            daily_price_data.append(new_data)

        df = pd.DataFrame(daily_price_data)

        csv_file = f"{self.data_path}/raw/price_data.csv"
        if not os.path.exists(csv_file):
            df.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, mode='a', header=False, index=False)

    def fetch_weather_data(self):
        response = requests.get(self.weather_url)
        response.raise_for_status()
        data = response.json()['hourly']

        daily_weather_data = []
        for i in range(len(data['time'])):
            temperature = data['temperature_2m'][i]
            humidity = data['relative_humidity_2m'][i]
            precipitation = data['precipitation'][i]
            cloud_cover = data['cloud_cover'][i]
            wind_speed = data['wind_speed_10m'][i]

            new_data = {'date': data['time'][i], 'temperature': temperature, 'humidity': humidity,
                        'precipitation': precipitation, 'cloud_cover': cloud_cover, 'wind_speed': wind_speed}
            daily_weather_data.append(new_data)

        df_weather = pd.DataFrame(daily_weather_data)

        csv_file = f"{self.data_path}/raw/weather_data.csv"
        if not os.path.exists(csv_file):
            df_weather.to_csv(csv_file, index=False)
        else:
            df_weather.to_csv(csv_file, mode='a', header=False, index=False)

    def fetch_production_data(self):
        response = requests.get(self.production_url)
        response.raise_for_status()
        data = response.json()

        production_types = [
            'Cross border electricity trading',
            'Nuclear',
            'Hydro Run-of-River',
            'Fossil brown coal / lignite',
            'Fossil gas',
        ]

        for i in range(len(data['production_types'])):
            if data['production_types'][i]['name'] not in production_types:
                continue

            production_per_type = []
            for j in range(len(data['production_types'][i]['data'])):
                production = data['production_types'][i]['data'][j]
                timestamp = datetime.fromtimestamp(data['unix_seconds'][j]).strftime('%Y-%m-%dT%H:%M:%S')

                production_per_type.append({'date': timestamp, 'production': production})

            df_production = pd.DataFrame(production_per_type)

            file_name = data['production_types'][i]['name'].replace(' ', '_').replace('/', '').lower()
            csv_file = f"{self.data_path}/raw/production_{file_name}_data.csv"
            if not os.path.exists(csv_file):
                df_production.to_csv(csv_file, index=False)
            else:
                df_production.to_csv(csv_file, mode='a', header=False, index=False)


def main():
    fetcher = Fetcher()
    fetcher.fetch_price_data()
    fetcher.fetch_weather_data()
    fetcher.fetch_production_data()


if __name__ == "__main__":
    main()
