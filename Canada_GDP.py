##CANADA GDP ANALYSIS##

##IMPORT LIBRARIES

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing

##LOAD CLEAN DATA

#This defines the dataframe (df) and will use the Pandas function 'read_excel' to access the data in the .CSV File
df = pd.read_excel(r'C:\Users\danhe\OneDrive\Data Science BSC\Professional Practice\Projects\Idea 1 - Cannabis Legislisation in Canada\Canada GDP\Canada GDP - CLEAN.xlsx', sheet_name='Sheet1', skiprows=0)
print(df.columns.tolist()) #CHECK THE COLUMN HEADERS - IMPORTANT FOR REST OF SCRIPT THAT THEY MATCH THE years and NAICS definitions
##PERFORM DATA CLEANSING TASKS

#Change column names from source to clean/normal data periods for analysis

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

#Define industries based on NAICS data
gdp_all = df.loc[df['NAICS'] == 'All industries', years].values.flatten()
gdp_cannabis = df.loc[df['NAICS'] == 'Cannabis sector', years].values.flatten()
gdp_rest = df.loc[df['NAICS'] == 'All industries (except cannabis sector)', years].values.flatten()

##DEFINE TIME SERIES ANALYSIS DEFINITIONS

years_int = [int(y) for y in years]
ts_all = pd.Series(gdp_all, index=years_int)
ts_cannabis = pd.Series(gdp_cannabis, index=years_int)
ts_rest = pd.Series(gdp_rest, index=years_int)

##PERFORM 5 YEAR FORECAST

forecast_years = list(range(years_int[-1]+1, years_int[+1]+6))

def forecast_series(ts, steps=5):
    #EXPONTENTIAL SMOOTHING CARRIED OUT ON DATA
    model = ExponentialSmoothing(ts, trend='add', seasonal=None)
    fit = model.fit()
    forecast = fit.forecast(steps)
    return forecast

forecast_all = forecast_series(ts_all)
forecast_cannabis = forecast_series(ts_cannabis)
forecast_rest = forecast_series(ts_rest)

##COMBINE ACTUAL AND FORECAST DATA FOR PRESENTING BACK

years_int = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]  # 9 years
forecast_years = [2026, 2027, 2028, 2029, 2030]  # 5 years
# ts_all should have 9 values, forecast_all should have 5 values
all_years = years_int + forecast_years  # 14 years
all_gdp = list(ts_all) + list(forecast_all)  # 14 values
cannabis_gdp = list(ts_cannabis) + list(forecast_cannabis)
rest_gdp = list(ts_rest) + list(forecast_rest)


##PLOT DEBUG

print(len(all_years), len(all_gdp))
print(all_years)
print(all_gdp)


##PLOT RESULTS

plt.figure(figsize=(10,6))
plt.plot(all_years, all_gdp, label='All Industries')
plt.plot(all_years, cannabis_gdp, label='Cannabis Sector')
plt.plot(all_years, rest_gdp, label='All Except Cannabis')
plt.axvline(years_int[-1], color='gray', linestyle='--', label='Forecast Start')
plt.title('GDP Forecast: Cannabis Sector vs Rest of Economy')
plt.xlabel('Year')
plt.ylabel('GDP')
plt.legend()
plt.tight_layout()
plt.show()

##IMPACT ASSESSMENT
impact = pd.Series(cannabis_gdp) / pd.Series(all_gdp)
print("Projected cannabis sector share of GDP for next 5 years:")
for year, pct in zip(forecast_years, impact[-5:]):
    print(f"{year}: {pct:.4%}")

