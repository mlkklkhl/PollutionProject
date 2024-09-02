import pandas as pd
import os, warnings

warnings.simplefilter("ignore")

if __name__ == "__main__":

    # Set the frequency of the data
    # Work with '1H' for hourly data, '1D' for daily data, '1W' for weekly data
    # **3H does not work because of the weather data is stamp at 1:00, 4:00, 7:00, 10:00, 13:00, 16:00, 19:00, 22:00
    freq = '1H'

    # Set the interpolation method
    method = 'spline'
    deg = 1

    # read the data
    df = pd.read_csv("combined_data.csv", encoding="utf8")

    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
    df.set_index('DateTime', inplace=True)

    # remove duplicate rows
    df = df[~df.index.duplicated(keep='first')]

    # resample the data
    df = df.resample(freq).asfreq()

    print("Dataframe information: ")
    print(df.describe().to_string(), '\n')
    print(df.isnull().sum().to_string(), '\n')

    df_list = []
    df_null_columns = df.columns

    # Save the data to a csv file
    df.to_csv('combined_data_upsampled_pm_' + freq + '.csv', index=True)

    # use spline interpolation to fill the missing data in the columns with NaN values
    print("Interpolating the data using ", method, " method with degree ", deg, "...\n")
    for i in df_null_columns:
        print("column: ", i)
        start, end = None, None
        isNull_start, isNull_end = False, False
        last = 0

        for ind in df[i].index:

            # check if the data is NaN
            if pd.isnull(df[i][ind]):
                isNull_start = True
            elif isNull_start and not pd.isnull(df[i][ind]):
                isNull_end = True
                end = ind
            else:
                start = ind

            # if the start and end index are found, interpolate the data
            if isNull_start:
                # if the end index is found, interpolate the data
                if isNull_end:
                    data_in = df[i].loc[start:end]

                    # if the data is not all NaN, interpolate the data
                    try:
                        i_min = data_in.min()
                        i_max = data_in.max()

                        data_in = data_in.interpolate(method=method, order=deg, limit_direction='both').clip(
                            lower=i_min,
                            upper=i_max)

                        df[i].loc[start:end] = data_in
                        isNull_start, isNull_end = False, False
                        start, end = ind, None

                        last = data_in.mean()
                    except:
                        continue

                # if the last value in dataframe is still NaN, fill it with the last non-null value
                elif not isNull_end and ind == df[i].index[-1]:
                    df[i].loc[start:end] = last

            else: last = df[i][ind]

    df['Day'] = df.index.day
    df['Year'] = df.index.year
    df['Month'] = df.index.month_name()

    print("Interpolated Dataframe information: ")
    print(df.describe().to_string())

    df.to_csv('combined_data_upsampled_pm_' + freq + '_' + method + '_' + str(deg) + 'degree.csv', index=True)

    print('------- finish --------')
