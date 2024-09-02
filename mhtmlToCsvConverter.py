import email
import csv
import os
import glob
import pandas as pd
import re
from bs4 import BeautifulSoup

def mhtml_to_csv(mhtml_file, csv_file):

    print(f"Processing MHTML file: {mhtml_file}")


    # Read the .mhtml file
    with open(mhtml_file, 'r', encoding='utf-8') as f:
        mhtml_content = f.read()

    # Parse the MHTML content
    msg = email.message_from_string(mhtml_content)

    # Find the HTML part
    html_part = None
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_part = part.get_payload(decode=True)
            break

    if not html_part:
        print("No HTML content found in the MHTML file.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(html_part, 'html.parser')

    # Extract data from the HTML (this part depends on your specific MHTML structure)
    # For this example, let's assume we're extracting data from a table
    table = soup.find('table')
    rows = table.find_all('tr')

    # Write data to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if os.path.basename(mhtml_file) == 'rainfall 2016-2024.mhtml':
            print("Rainfall")
            writer.writerow(
                ['No', 'Station', 'Date', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                 '31', 'Total'])
        else:
            writer.writerow(
                ['No', 'Station', 'Date', '0100', '0400', '0700', '1000', '1300', '1600', '1900', '2200', 'Total'])

        i = 0

        for row in rows:
            if i < 2:
                i += 1
                continue
            else:
                cols = row.find_all(['td', 'th'])
                writer.writerow([col.text.strip() for col in cols])

def transform_date(date_str):
    # Split the date string into parts
    month_year, day = date_str.split()
    month, year = month_year.split('/')
    # Pad the day with a leading zero if necessary
    day = day.zfill(2)

    # check if month is 30 days skip 31
    if month in ['4', '6', '9', '11'] and day == '31':
        return None
    # check if leap year
    elif month == '2':
        if day in ['29', '30', '31'] and (int(year) % 4 != 0 or (int(year) % 100 == 0 and int(year) % 400 != 0)):
            return None
        elif day in ['30', '31']:
            return None
    else:
        # Return the date in the format "dd/mm/yyyy"
        return f"{day}/{month.zfill(2)}/{year}"


def prep_dataframe(df, var, year):
    # Remove unnecessary columns
    df = df.drop(columns=['No', 'Station', 'Total'])

    if var == 'rainfall' and year == '2016-2024':
        # Get day slot columns
        day_slots = [col for col in df.columns if re.match(r'\d{2}', col)]
        print("Day slots columns:", day_slots)


        # Melt the DataFrame
        df_melted = pd.melt(df, id_vars=['Date'], value_vars=day_slots, var_name='Day', value_name=var)

        df_melted['DateTime'] = df_melted['Date'] + ' ' + df_melted['Day']
        df_melted['DateTime'] = df_melted['DateTime'].apply(transform_date)

        df_melted = df_melted.dropna()
        df_melted['Time'] = '0100'
        df_melted['DateTime'] = df_melted['DateTime'] + ' ' + df_melted['Time']
        df_melted['DateTime'] = pd.to_datetime(df_melted['DateTime'], format='%d/%m/%Y %H%M')
        df_melted = df_melted.drop(columns=['Date', 'Day', 'Time'])

    else:
        # Get time slot columns
        time_slots = [col for col in df.columns if re.match(r'\d{2}:?\d{2}', col)]

        # Melt the DataFrame
        df_melted = pd.melt(df, id_vars=['Date'], value_vars=time_slots, var_name='Time', value_name=var)

        # Transform Time column to 24-hour format with leading zeros
        df_melted['Time'] = df_melted['Time'].str.zfill(4)

        df_melted['DateTime'] = df_melted['Date'] + ' ' + df_melted['Time']
        df_melted['DateTime'] = pd.to_datetime(df_melted['DateTime'], format='%d/%m/%Y %H%M')
        df_melted = df_melted.drop(columns=['Date', 'Time'])

    # Replace var column with '-' to 0 and 'T' to 0.1
    df_melted[var] = df_melted[var].replace('-', 0)
    df_melted[var] = df_melted[var].replace('T', 0.1)

    # set index to DateTime
    df_melted.set_index('DateTime', inplace=True)

    # sort index
    df_melted.sort_index(inplace=True)

    return df_melted


if __name__=="__main__":
    # find .mhtml file in raw_data folder
    mhtml_files = glob.glob('weather/raw_data/*.mhtml')

    # Create prep_data folder if it doesn't exist
    os.makedirs('weather/prep_data', exist_ok=True)

    for mhtml_file in mhtml_files:
        print(f"Converting {mhtml_file} to CSV...")

        csv_file = os.path.join('weather', 'prep_data', os.path.basename(mhtml_file).replace('.mhtml', '.csv'))
        mhtml_to_csv(mhtml_file, csv_file)

        df = pd.read_csv(csv_file)

        var = os.path.basename(mhtml_file).split(' ')[0]
        year = os.path.basename(mhtml_file).split(' ')[1].replace('.mhtml', '')
        print(var, year)
        df_melted = prep_dataframe(df, var, year)

        df_melted.to_csv(csv_file, index=True)

        print(f"Finish {mhtml_file} to CSV... \n")

    print("Finished converting all MHTML files to CSV \n")

