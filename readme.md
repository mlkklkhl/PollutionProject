```
 The `readme.md` file is used to provide the information about the project. It is written in markdown language. The content of the `readme.md` file is as follows:
```

# Data Preprocessing for Pollution Project

![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit-learn-013243?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)
![MIT](https://img.shields.io/badge/license-MIT-013243?style=for-the-badge&logo=license&logoColor=white)

## Introduction

The data used in this project are from two main sources:

1. Weather Data from Thai Meteorological Department: directory `weather/raw_data`
2. Pollution Data from Air4Thai: directory `PM2.5/raw_data`

## Data Preprocessing

The data preprocessing is done in the following steps:

1. Weather Data Preprocessing: the data are .mhtml files that need to be converted to .csv files. This step is done in
   the `mhtmlToCsvConverter.py`. The resulted .csv files are stored in the `weather/prep_data` directory.
2. Pollution Data Preprocessing: the data are .xlsx files that need to be converted to .csv files. This step is done in
   the `xlsxToCsvConverter.py`. The resulted .csv files are stored in the `PM2.5/prep_data` directory.
3. Merging Data: the weather and pollution data are merged based on the date and time. This step is done in
   the `combine_data.py`. It has 3 main steps:
    - `combine_weather`: this function merges the weather data based on the date and time. This step combine and create
      a new .csv file named `combined_weather_data.csv`.
    - `combine_pm_air4thai`: this function merges the pm2.5 data based on the date and time. This step combine and
      create a new .csv file named `combined_pm2.5A_data.csv`.
    - Finally, the main function combines both weather and pm2.5 data based on the date and time. The resulted file is
      named `combined_data.csv`.
4. Data Cleaning: the data are cleaned by replacing the rows with missing values with interpolation technique. Moreover,
   it resample the data into hourly. This step is done in the `interpolate_data.py`. The resulted file is
   named `combined_data_upsampled_pm_1hour_final-all-spline.csv`.

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
3. Bukhoree Sahoh (Leader)
4. Mallika Kliangkhlao (Member)
5. Apaporn Tipsavak (Member)

## Contributors

<a href="https://github.com/mlkklkhl">
  <img src="https://github.com/mlkklkhl.png" alt="mlkklkhl" width="60" height="60" style="border-radius: 50%;">
</a>
<a href="https://github.com/bukhoree">
  <img src="https://github.com/bukhoree.png" alt="bukhoree" width="60" height="60" style="border-radius: 50%;">
</a>
<a href="https://github.com/apaporn">
  <img src="https://github.com/apaporn.png" alt="apaporn" width="60" height="60" style="border-radius: 50%;">
</a>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
