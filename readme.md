
```
 The `readme.md` file is used to provide the information about the project. It is written in markdown language. The content of the `readme.md` file is as follows:
```

# Data Preprocessing for Pollution Project

## Introduction
The data used in this project are from two main sources:
1. Weather Data from Thai Meteorological Department: directory `weather/raw_data`
2. Pollution Data from Air4Thai: directory `PM2.5/raw_data`

## Data Preprocessing
The data preprocessing is done in the following steps:
1. Weather Data Preprocessing: the data are .mhtml files that need to be converted to .csv files. This step is done in the `mhtmlToCsvConverter.py`. The resulted .csv files are stored in the `weather/prep_data` directory.
2. Pollution Data Preprocessing: the data are .xlsx files that need to be converted to .csv files. This step is done in the `xlsxToCsvConverter.py`. The resulted .csv files are stored in the `PM2.5/prep_data` directory.
3. Merging Data: the weather and pollution data are merged based on the date and time. This step is done in the `combine_data.py`. It has 3 main steps:
    - `combine_weather`: this function merges the weather data based on the date and time. This step combine and create a new .csv file named `combined_weather_data.csv`.
    - `combine_pm_air4thai`: this function merges the pm2.5 data based on the date and time. This step combine and create a new .csv file named `combined_pm2.5A_data.csv`.
    - Finally, the main function combines both weather and pm2.5 data based on the date and time. The resulted file is named `combined_data.csv`.
4. Data Cleaning: the data are cleaned by replacing the rows with missing values with interpolation technique. Moreover, it resample the data into hourly. This step is done in the `interpolate_data.py`. The resulted file is named `combined_data_upsampled_pm_1hour_final-all-spline.csv`.

## Dependencies
The dependencies are listed in the `requirements.txt` file. To install the dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Usage
To run the data preprocessing, run the following command:
```bash
python mhtmlToCsvConverter.py
python xlsxToCsvConverter.py
python combine_data.py
python interpolate_data.py
```

## Acknowledgements
1. [Thai Meteorological Department](https://www.tmd.go.th/)
2. [Air4Thai](https://air4thai.pcd.go.th/)
3. Bukhoree Sahoh (Leader a.k.a Big Boss)
4. Mallika Kliangkhlao (Member)
5. Apaporn Tipsavak (Member)

## Contributors
1. [<img src="https://github.com/{{ mlkklkhl }}.png" width="60px;"/><br /><sub><ahref="https://github.com/{{ mlkklkhl }}">{{ mlkklkhl }}</a></sub>](https://github.com/{{ mlkklkhl }}/{{ repository }}
2. [bukhoree](Bukhoree Sahoh)
3. [apaporn](Apapon Tipsavak)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





