import pandas as pd

# Load the day data file
day_data = pd.read_csv("SampleDayData.csv")
# Load the intraday data for 19th April
intraday_data_19 = pd.read_csv("19thAprilSampleData.csv")
# Load the intraday data for 22nd April
intraday_data_22 = pd.read_csv("22ndAprilSampleData.csv")

# Check for NaN values in each DataFrame
print("NaN values in SampleDayData.csv:")
print(day_data.isna().sum())

print("\nNaN values in 19thAprilSampleData.csv:")
print(intraday_data_19.isna().sum())

print("\nNaN values in 22ndAprilSampleData.csv:")
print(intraday_data_22.isna().sum())
