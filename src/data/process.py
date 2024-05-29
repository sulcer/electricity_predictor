import os

import pandas as pd


def main():
    price_data = 'price_data.csv'
    weather_data = 'weather_data.csv'

    df_price = pd.read_csv(f'data/raw/{price_data}')
    df_weather = pd.read_csv(f'data/raw/{weather_data}')

    # price data
    merge_data(df_price, df_weather, 'price',
               ['temperature', 'humidity', 'precipitation', 'cloud_cover', 'wind_speed'], price_data)

    # production data
    for file in os.listdir('data/raw'):
        if file.startswith('production_') and file.endswith('data.csv'):
            df_production = pd.read_csv(f'data/raw/{file}')
            merge_data(df_production, df_weather, 'production',
                       ['temperature', 'humidity', 'precipitation', 'cloud_cover', 'wind_speed'], file)


def merge_data(df, df_weather, target_feature, features, output_file_name):
    df['date'] = pd.to_datetime(df['date'])
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    validate_merge(24, df, output_file_name)

    merged_df = pd.merge(df, df_weather, on='date')

    selected_features = [target_feature] + features

    output_file = f'data/processed/{output_file_name}'
    if os.path.exists(output_file):
        merged_df[selected_features].to_csv(output_file, mode='a', header=False, index=False)
    else:
        merged_df[selected_features].to_csv(output_file, index=False)


def validate_merge(window_size, df, file_name):
    print(f"[INFO] {file_name}")
    check_data_path = f'data/processed/{file_name}'
    if os.path.exists(check_data_path):
        check_data = pd.read_csv(check_data_path)
    else:
        check_data = []

    num_of_processed_fetches = len(check_data) / window_size
    num_of_fetches = len(df) / window_size

    print("[INFO] Number of processed fetches", num_of_processed_fetches)
    print("[INFO] Number of fetches", num_of_fetches)

    if num_of_fetches <= num_of_processed_fetches:
        raise ValueError("Cannot merge data, if no new data has been fetched")


if __name__ == '__main__':
    main()
