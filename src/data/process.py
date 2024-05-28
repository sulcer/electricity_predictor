import os

import pandas as pd


def main():
    price_data = 'price_data.csv'
    weather_data = 'weather_data.csv'
    production_data = []
    for file in os.listdir('data/raw'):
        if file.startswith('production_') and file.endswith('data.csv'):
            production_data.append(file)

    df_price = pd.read_csv(f'data/raw/{price_data}')
    df_weather = pd.read_csv(f'data/raw/{weather_data}')

    merge_data(df_price, df_weather, 'price',
               ['temperature', 'humidity', 'precipitation', 'cloud_cover', 'wind_speed'], price_data)

    for file in production_data:
        df_production = pd.read_csv(f'data/raw/{file}')
        merge_data(df_production, df_weather, file.split('_')[1],
                   ['temperature', 'humidity', 'precipitation', 'cloud_cover', 'wind_speed'], file)


def merge_data(df, df_weather, target_feature, features, output_file_name):
    df['date'] = pd.to_datetime(df['date'])
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    merged_df = pd.merge(df, df_weather, on='date')

    # TODO: simple validation

    selected_features = [target_feature] + features

    output_file = f'data/processed/{output_file_name}'
    if os.path.exists(output_file):
        merged_df[selected_features].to_csv(output_file, mode='a', header=False, index=False)
    else:
        merged_df[selected_features].to_csv(output_file, index=False)


if __name__ == '__main__':
    main()
