import glob
import itertools
import os
import pandas as pd

def aggregate_data(data):
    # set the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data['DateTime'] = data['DateTime'].dt.date

    # set the DateTime column as the index
    data.set_index('DateTime', inplace=True)

    # aggregate the data
    for i in data.columns:
        if i != 'DateTime':
            if i != 'PM2.5_NanoSampler' and i != 'PM2.5' and i != 'PM10' and i != 'rainfall':
                # calculate the mean, max, min, and standard deviation of each column
                data[i + '_Mean'] = data.groupby('DateTime')[i].transform('mean')
                data[i + '_Max'] = data.groupby('DateTime')[i].transform('max')
                data[i + '_Min'] = data.groupby('DateTime')[i].transform('min')
                data[i + '_SD'] = data.groupby('DateTime')[i].transform('std')
            else:
                data[i + '_Mean'] = data.groupby('DateTime')[i].transform('mean')

    # select only the _Mean, _Max, _Min, _SD columns
    data = data.filter(regex='Mean|Max|Min|SD')

    return data

if __name__ == "__main__":
    # Read the data
    weather_data = pd.read_csv('combined_weather_data.csv', index_col='DateTime', parse_dates=True)
    pm25A_data = pd.read_csv('combined_pm2.5A_data.csv', index_col='DateTime', parse_dates=True)
    pm10A_data = pd.read_csv('combined_pm10A_data.csv', index_col='DateTime', parse_dates=True)
    pm_nanosampler_data = pd.read_csv('combined_Hatyai_PM0.1_data.csv', parse_dates=True)

    # merge data based on pm_nanosampler_data date index
    # transform the DateTime index to date index
    combine_data_2 = pm_nanosampler_data.copy()

    # set the DateTime column to datetime format
    combine_data_2['DateTime'] = pd.to_datetime(combine_data_2['DateTime'], format='%Y-%m-%d %H:%M:%S')
    combine_data_2['DateTime'] = combine_data_2['DateTime'].dt.date

    # print date range
    print("Date range:")
    print(f"combine_data_2: {combine_data_2.DateTime.min()} - {combine_data_2.DateTime.max()}")

    # aggregate the data
    weather_data_2 = aggregate_data(weather_data)
    pm25A_data_2 = aggregate_data(pm25A_data)
    pm10A_data_2 = aggregate_data(pm10A_data)

    # print data description
    print("\nWeather data 2 description:")
    print(weather_data_2.head().to_string(), '\n')

    print("PM2.5A data 2 description:")
    print(pm25A_data_2.head().to_string(), '\n')

    print("PM10A data 2 description:")
    print(pm10A_data_2.head().to_string(), '\n')

    # merge the weather data with pm_nanosampler_data based on pm_nanosampler_data date index
    combine_data_2 = pd.merge(combine_data_2, weather_data_2, on='DateTime', how='outer')
    combine_data_2 = pd.merge(combine_data_2, pm25A_data_2, on='DateTime', how='outer')
    combine_data_2 = pd.merge(combine_data_2, pm10A_data_2, on='DateTime', how='outer')

    # sort the DataFrame by the DateTime index
    combine_data_2.set_index('DateTime', inplace=True)
    combine_data_2.sort_values(by='DateTime', inplace=True)

    # drop duplicate rows
    combine_data_2 = combine_data_2.loc[~combine_data_2.index.duplicated(keep='first')]
    combine_data_2 = combine_data_2[combine_data_2['temperature_Mean'] != 0]
    combine_data_2 = combine_data_2[combine_data_2['PM0.1'].notna()]

    # set index to DateTime index
    combine_data_2.index = pd.to_datetime(combine_data_2.index)

    print("Combined data 2 description:")
    print(combine_data_2.head().to_string(), '\n')
    print(f"data: {combine_data_2.index.min()} - {combine_data_2.index.max()}")

    # Save the combined data to a single CSV file
    combine_data_2.to_csv('combined_data_based_on_nanosampler.csv')

    print(f"Finish saving combined data to CSV file combined_data_based_on_nanosampler.csv")