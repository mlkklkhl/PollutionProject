import pandas as pd
import os, warnings

warnings.simplefilter("ignore")

if __name__ == "__main__":

    df = pd.read_csv("combined_data.csv", encoding="utf8")

    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
    df.set_index('DateTime', inplace=True)

    df = df[~df.index.duplicated(keep='first')]

    freq = '1H'
    df = df.resample(freq).asfreq()

    print("Dataframe information: ")
    print(df.describe().to_string(), '\n')
    print(df.isnull().sum().to_string(), '\n')

    df_list = []
    df_null_columns = df.columns

    print("columns with NaN values: ")
    print(df_null_columns, '\n')

    df.to_csv('combined_data_upsampled_pm_' + freq + '.csv', index=True)

    # use spline interpolation to fill the missing data in the columns with NaN values
    for i in df_null_columns:
        print("column: ", i)
        start, end = None, None
        isNull_start, isNull_end = False, False
        last = 0

        for ind in df[i].index:

            if pd.isnull(df[i][ind]):
                isNull_start = True
            elif isNull_start and not pd.isnull(df[i][ind]):
                isNull_end = True
                end = ind
            else:
                start = ind

            if isNull_start:
                if isNull_end:
                    data_in = df[i].loc[start:end]

                    if i == 'PM2.5A':
                        print(data_in)

                    try:
                        i_min = data_in.min()
                        i_max = data_in.max()

                        data_in = data_in.interpolate(method='spline', order=1, limit_direction='both').clip(
                            lower=i_min,
                            upper=i_max)

                        df[i].loc[start:end] = data_in
                        isNull_start, isNull_end = False, False
                        start, end = ind, None

                        last = data_in.mean()
                    except:
                        continue

                elif not isNull_end and ind == df[i].index[-1]:
                    print("last: ", last)
                    df[i].loc[start:end] = last

df['Day'] = df.index.day
df['Year'] = df.index.year
df['Month'] = df.index.month_name()

print("Interpolated Dataframe information: ")
print(df.describe().to_string())

method = 'spline'
df.to_csv('combined_data_upsampled_pm_' + freq + '_' + method + '.csv', index=True)

print('------- finish --------')
