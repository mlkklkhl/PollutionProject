import glob
import itertools
import os
import pandas as pd

def combine_weather():
    # Merge all CSV files into a single DataFrame based on DateTime index and save it as a single CSV file
    csv_files = glob.glob('weather/prep_data/*.csv')
    combined_data = pd.DataFrame()

    for csv_file in csv_files:
        print(f"Reading {csv_file}...")
        df = pd.read_csv(csv_file, index_col='DateTime', parse_dates=True)
        # join the DataFrame to the combined_data DataFrame if they have duplicate columns then merge them
        combined_data = pd.concat([combined_data, df], axis=0)

    # convert duplicate datetime index rows to a single row by taking the max of the values
    combined_data = combined_data.groupby(combined_data.index).max()

    # Sort the DataFrame by the DateTime index
    combined_data.sort_index(inplace=True)

    # Save the combined data to a single CSV file
    combined_data.to_csv('combined_weather_data.csv')

    return combined_data


def combine_pm_air4thai(path):
    combined_data = pd.DataFrame()

    print(f"\nReading {path} data...")
    csv_files = glob.glob(path + '/prep_data/*.csv')

    for csv_file in csv_files:

        print(f"Reading {csv_file}...")
        df = pd.read_csv(csv_file)

        if csv_file != path + '/prep_data\\PM2.5(2024).csv':
            # if the column 44T exists then rename it to PM2.5A
            if '44T ' in df.columns:
                df = df.rename(columns={'44T ': '44T'})

            # rename column 44T to PM2.5A
            df = df.rename(columns={'44T': path})

            # drop rows with missing values in 44T column
            df = df.dropna(subset=[path])

            # check if df['Date'] is in datetime format='%Y-%m-%d %H:%M:%S'
            try:
                df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            except:
                # Replace '/' with '-' in the Date column
                df['Date'] = df['Date'].str.replace('/', '-')

                # Convert to datetime, assuming day-first format if it contains '-'
                df['DateTime'] = pd.to_datetime(df['Date'], dayfirst=df['Date'].str.contains('-').any())

                # Set the time to 00:00:00 for all dates
                df['DateTime'] = df['DateTime'].dt.normalize()
                df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')

            # check if DateTime is 00:00:00 then change to 01:00:00
            df.loc[df['DateTime'].dt.hour == 0, 'DateTime'] = df['DateTime'] + pd.DateOffset(hours=1)
            df = df[['DateTime', path]]

        else:
            # rename 1st column to Date and 2nd column to Time
            df = df.rename(columns={df.columns[1]: 'Date', df.columns[2]: 'Time'})
            df = df.rename(columns={'pm2.5': path})

            # merge 2 and 3 columns into datetime using column index
            df['DateTime'] = df['Date'] + ' ' + df['Time']
            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')

            df = df[['DateTime', path]]

        # encode categorical data to float data type
        for i in df.columns:
            # check if the data type is object
            if df[i].dtype == 'object' and i != 'DateTime':
                # convert the data type to float if the data is ' ' then replace it with null
                df[i] = pd.to_numeric(df[i], errors='coerce')

        combined_data = pd.concat([combined_data, df], axis=0)

    # convert datetime index to DateTime index to %H:%M
    combined_data.set_index('DateTime', inplace=True)
    combined_data.sort_index(inplace=True)

    # Save the combined data to a single CSV file
    combined_data.to_csv('combined_' + path + 'A_data.csv')

    return combined_data


def combine_nanosampler(path):
    print(f"\nReading {path} data...")
    csv_files = glob.glob(path + '/prep_data/*.csv')

    # find unique prefix of csv_files
    unique_prefix = set([os.path.basename(csv_file).split('_')[0] for csv_file in csv_files])
    print(f"Unique prefix: {unique_prefix}")

    # create dict of each unique prefix which prefix is the key and value is the list of csv_files
    prefix_dict = {prefix: [csv_file for csv_file in csv_files if prefix in csv_file] for prefix in unique_prefix}
    print(f"Prefix dict: {prefix_dict}")

    for prefix, csv_files in prefix_dict.items():
        combined_data = pd.DataFrame()
        print(f"\nReading {prefix} data...")
        for csv_file in csv_files:
            print(f"Reading {csv_file}...")
            df = pd.read_csv(csv_file)
            df = df.rename(columns={'Date': 'DateTime', 'PM2.5': 'PM2.5_NanoSampler'})
            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
            combined_data = pd.concat([combined_data, df], axis=0)

        # convert datetime index to DateTime index to %H:%M
        combined_data.set_index('DateTime', inplace=True)
        combined_data.sort_index(inplace=True)

        # Save the combined data to a single CSV file
        combined_data.to_csv('combined_' + prefix + '_' + path + '_data.csv')

if __name__ == "__main__":
    weather_data = combine_weather()
    pm25A_data = combine_pm_air4thai("PM2.5")
    pm10A_data = combine_pm_air4thai("PM10")
    combine_nanosampler("PM0.1")

    # read Hatyai data from CSV file
    pm_nanosampler_data = pd.read_csv('combined_Hatyai_PM0.1_data.csv')
    # set the DateTime column to datetime format
    pm_nanosampler_data['DateTime'] = pd.to_datetime(pm_nanosampler_data['DateTime'], format='%Y-%m-%d %H:%M:%S')

    weather_data.reset_index(inplace=True)
    pm25A_data.reset_index(inplace=True)
    pm10A_data.reset_index(inplace=True)

    # print data description
    print("Weather data description:")
    print(weather_data.describe().to_string(), '\n')

    print("PM2.5A data description:")
    print(pm25A_data.describe().to_string(), '\n')

    print("PM10A data description:")
    print(pm10A_data.describe().to_string(), '\n')

    print("PM0.1 data description:")
    print(pm_nanosampler_data.describe().to_string(), '\n')

    # concat the weather and PM2.5A data
    combined_data = pd.merge(weather_data, pm25A_data, on='DateTime', how='outer')
    combined_data = pd.merge(combined_data, pm10A_data, on='DateTime', how='outer')
    combined_data = pd.merge(combined_data, pm_nanosampler_data, on='DateTime', how='outer')

    # sort the DataFrame by the DateTime index
    combined_data.set_index('DateTime', inplace=True)
    combined_data.sort_values(by='DateTime', inplace=True)

    # drop rows if temperature is 0
    combined_data = combined_data[combined_data['temperature'] != 0]

    # print combined data description
    print("Combined data description:")
    print(combined_data.describe().to_string(), '\n')

    # Save the combined data to a single CSV file
    combined_data.to_csv('combined_data.csv')

    print(f"Finish saving combined data to CSV file combined_data.csv")
