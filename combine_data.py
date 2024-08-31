import glob
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


def combine_pm_air4thai():
    combined_data = pd.DataFrame()

    csv_files = glob.glob('PM2.5/prep_data/*.csv')

    for csv_file in csv_files:

        print(f"Reading {csv_file}...")
        df = pd.read_csv(csv_file)

        if csv_file != 'PM2.5\\prep_data\\PM2.5(2024).csv':
            # if the column 44T exists then rename it to PM2.5A
            if '44T ' in df.columns:
                df = df.rename(columns={'44T ': '44T'})

            # rename column 44T to PM2.5A
            df = df.rename(columns={'44T': 'PM2.5A'})

            # drop rows with missing values in 44T column
            df = df.dropna(subset=['PM2.5A'])

            # change 00:00 to 01:00
            df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            df['DateTime'] = df['DateTime'] + pd.DateOffset(hours=1)
            df = df[['DateTime', 'PM2.5A']]

        else:
            # merge 2 and 3 columns into datetime using column index
            df['DateTime'] = df.iloc[:, 1] + ' ' + df.iloc[:, 2]

            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
            df = df.rename(columns={'pm2.5': 'PM2.5A'})
            df = df[['DateTime', 'PM2.5A']]

        # print df row count
        print(df.shape[0], '\n')
        combined_data = pd.concat([combined_data, df], axis=0)

    # convert datetime index to DateTime index to %H:%M
    combined_data.set_index('DateTime', inplace=True)
    combined_data.sort_index(inplace=True)

    # Save the combined data to a single CSV file
    combined_data.to_csv('combined_pm2.5A_data.csv')

    return combined_data


if __name__ == "__main__":
    # weather_data = combine_weather()
    # pmA_data = combine_pm_air4thai()

    weather_data = pd.read_csv('combined_weather_data.csv')
    pmA_data = pd.read_csv('combined_pm2.5A_data.csv')

    # set index to DateTime
    weather_data['DateTime'] = pd.to_datetime(weather_data['DateTime'])
    weather_data.set_index('DateTime', inplace=True)

    pmA_data['DateTime'] = pd.to_datetime(pmA_data['DateTime'])
    pmA_data.set_index('DateTime', inplace=True)

    combined_data = pd.merge(weather_data, pmA_data, left_index=True, right_index=True, how='left')
    combined_data.to_csv('combined_data.csv')

    print(f"Finish saving combined data to CSV file combined_data.csv")
