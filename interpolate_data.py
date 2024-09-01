import pandas as pd
import os, warnings

warnings.simplefilter("ignore")

if __name__ == "__main__":
    
    df = pd.read_csv("combined_data.csv", encoding="utf8")
    
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
    df.set_index('DateTime', inplace=True)
    
    df = df[~df.index.duplicated(keep='first')]
    
    # df object column to float
    for i in df.columns:
        if df[i].dtype == 'object':
            df[i] = df[i].str.replace(',', '.').astype(float)

    print('----- Resampling ------')
    # resample df to 1 hour and fill with blank
    df = df.resample('1H').asfreq()
    
    print(df.isnull().sum().to_string())
    print(df.describe().to_string())
    
    print('----- Interpolating ------')
    
    df_list = []
    df_null_columns = df.columns
    
    for i in df_null_columns:
        print("column: ", i)
        start, end = None, None
        isNull_start, isNull_end = False, False
    
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
                    i_min = data_in.min()
                    i_max = data_in.max()
    
                    data_in = data_in.interpolate(method='spline', order=1, limit_direction='both').clip(lower=i_min,
                                                                                                    upper=i_max)
    
                    df[i].loc[start:end] = data_in
                    isNull_start, isNull_end = False, False
                    start, end = None, None
    
                elif not isNull_end and ind == df[i].index[-1]:
                    data_in = df[i].loc[start:ind]
                    i_min = df[i].min()
                    i_max = df[i].max()
    
                    data_in = data_in.interpolate(method='spline', order=1, limit_direction='both').clip(lower=i_min,
                                                                                                    upper=i_max)
    
                    df[i].loc[start:end] = data_in
                    isNull_start, isNull_end = False, False
                    start, end = None, None
    
    df['Day'] = df.index.day
    df['Year'] = df.index.year
    df['Month'] = df.index.month_name()

    print('----- Data After Interpolation ------')
    print(df.describe().to_string())
    
    method = 'final-all-spline'
    df.to_csv('combined_data_upsampled_pm_1hour_' + method + '.csv', index=True)
    
    print('------- finish --------')
