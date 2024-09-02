import glob
import os
import pandas as pd

if __name__ == "__main__":
    xlsx_files = glob.glob('PM2.5/raw_data/*.xlsx')

    output_dir = 'PM2.5/prep_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory {output_dir} created.")

    for xlsx_file in xlsx_files:
        print(f"Reading {xlsx_file}...")
        read_file = pd.read_excel(xlsx_file)
        csv_file = os.path.join('PM2.5/prep_data', os.path.basename(xlsx_file).replace('.xlsx', '.csv'))
        read_file.to_csv(csv_file, index=None, header=True)

    print(f"Finish saving {xlsx_file} to CSV... \n")