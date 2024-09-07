import glob
import os
import pandas as pd

# function to find the starting and stopping date based on the week number and month in the year
def find_starting_stopping_date(week, month, year):

    # convert month to its number
    month = pd.to_datetime(month, format='%b').month

    # get the first day of the month
    starting_date = pd.to_datetime(f'{year}-{month}-01 01:00:00', format='%Y-%m-%d %H:%M:%S')
    starting_date = starting_date + pd.DateOffset(weeks=week)

    # get the last day of the week by add 6 days to the starting date
    stopping_date = starting_date + pd.DateOffset(days=6)

    return starting_date, stopping_date


if __name__ == "__main__":
    xlsx_files = glob.glob('PM0.1/raw_data/*.xlsx')

    for xlsx_file in xlsx_files:
        print(f"\nReading {xlsx_file}...")

        # Get the base name of the file after nanosampler prefix or Nanosampler (ug/m3) prefix
        base_name = os.path.basename(xlsx_file)
        if 'Nanosampler' in base_name:
            base_name = base_name.split('Nanosampler')[1]
        elif 'nanosampler' in base_name:
            base_name = base_name.split('nanosampler')[1]
        # remove .xlsx extension and trim the string
        base_name = base_name.split('.xlsx')[0].strip()

        # Read sheets in the xlsx file
        xls = pd.ExcelFile(xlsx_file)
        sheet_names = xls.sheet_names

        for sheet_name in sheet_names:

            print(f"\nProcessing {sheet_name}...")

            df = pd.read_excel(xls, sheet_name=sheet_name)
            df.columns = df.iloc[0]
            df.drop(df.index[0], inplace=True)

            # drop columns that have NaN value in PM0.1
            df = df.dropna(subset=['PM0.1'])

            # replace column Numbwr with Number
            df = df.rename(columns={'Numbwr': 'Number'})
            df = df.rename(columns={'Month ': 'Month'})
            df = df.rename(columns={'Stoping ': 'Stopping'})
            df = df.rename(columns={'PM0.1 ': 'PM0.1'})

            selected_columns = df[['Month', 'Number', 'Starting', 'Stopping', 'PM0.1', 'PM0.1-0.5', 'PM0.5-1.0',
                                   'PM1.0-2.5', 'PM2.5-10', 'PM>10', 'PM0.1', 'PM1', 'PM2.5']]

            print(selected_columns.head().to_string(), "\n")

            all_series = pd.DataFrame()
            month = 'N/A'

            for index, row in selected_columns.iterrows():

                if pd.isnull(row['Month']):
                    month = month
                else:
                    month = row['Month']

                if pd.isnull(row['Starting']) or pd.isnull(row['Stopping']):
                    # Generate starting and stopping date based on the Numbwr (week) of Month column in the year (sheet_name),
                    # like if number is 1 then starting_date is the first day of the first week of month in the year
                    # and stopping_date is the last day of the first week of month in the year
                    # replace # character from Numbwr and convert it to integer
                    week = int(row['Number'].replace('#', ''))

                    starting_date, stopping_date = find_starting_stopping_date(week, month, sheet_name)
                    print("Year: ", sheet_name, " Week: ", week, " Starting Date: ", starting_date, " - Stopping Date: ", stopping_date)
                else:
                    starting_date = row['Starting'] + pd.DateOffset(hours=1)
                    stopping_date = row['Stopping'] + pd.DateOffset(hours=1)

                # check if stopping date is over than starting date more than 7 days then replace month and date of stopping date
                if stopping_date - starting_date > pd.Timedelta(days=7):
                    print("Stopping date is over than starting date more than 7 days...")
                    print("Starting Date: ", starting_date, " Stopping Date: ", stopping_date)
                    stopping_date = starting_date + pd.Timedelta(days=7)
                    print("Replace Stopping Date: ", stopping_date)

                pm_value1 = row['PM0.1'].iloc[0]
                pm_value2 = row['PM0.1-0.5']
                pm_value3 = row['PM0.5-1.0']
                pm_value4 = row['PM1.0-2.5']
                pm_value5 = row['PM2.5-10']
                pm_value6 = row['PM>10']
                pm_value7 = row['PM1']
                pm_value8 = row['PM2.5'].iloc[0]

                # transform mix format of starting and stopping date to datetime 01:00:00
                starting_date = pd.to_datetime(starting_date, format='%Y-%m-%d %H:%M:%S')
                stopping_date = pd.to_datetime(stopping_date, format='%Y-%m-%d %H:%M:%S')

                print("Date: ", starting_date, ' - ', stopping_date)

                date_range = pd.date_range(start=starting_date, end=stopping_date)

                pm_series1 = [pm_value1] * len(date_range)
                pm_series2 = [pm_value2] * len(date_range)
                pm_series3 = [pm_value3] * len(date_range)
                pm_series4 = [pm_value4] * len(date_range)
                pm_series5 = [pm_value5] * len(date_range)
                pm_series6 = [pm_value6] * len(date_range)
                pm_series7 = [pm_value7] * len(date_range)
                pm_series8 = [pm_value8] * len(date_range)

                temp_df = pd.DataFrame(
                    {'Date': date_range, 'PM0.1': pm_series1, 'PM0.1-0.5': pm_series2, 'PM0.5-1.0': pm_series3,
                     'PM1.0-2.5': pm_series4, 'PM2.5-10': pm_series5, 'PM>10': pm_series6, 'PM1': pm_series7,
                     'PM2.5': pm_series8})

                all_series = pd.concat([all_series, temp_df], ignore_index=True)

            file_name = f"{sheet_name}.csv"
            file_path = f"PM0.1/prep_data/{base_name + '_' + file_name}"
            all_series.to_csv(file_path, index=False)
            print(f"Finish saving {file_name} to CSV...")

    print(f"Finish saving {xlsx_file} to CSV... \n")
