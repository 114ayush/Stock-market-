import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the day data file
day_data = pd.read_csv("SampleDayData.csv")
# Load the intraday data for 19th April
intraday_data_19 = pd.read_csv("19thAprilSampleData.csv")
# Load the intraday data for 22nd April
intraday_data_22 = pd.read_csv("22ndAprilSampleData.csv")

# Convert Date in day data to datetime for easier manipulation
day_data['Date'] = pd.to_datetime(day_data['Date'], format='%d/%m/%y', dayfirst=True)

# Define the target dates
target_dates = {
    '19-04-2024': datetime.strptime("19-04-2024", "%d-%m-%Y"),
    '22-04-2024': datetime.strptime("22-04-2024", "%d-%m-%Y")
}

# Calculate the start date (30 trading days prior)
start_date_19 = target_dates['19-04-2024'] - timedelta(days=30)
start_date_22 = target_dates['22-04-2024'] - timedelta(days=30)

# Filter day data for the 30 days before each target date
day_data_30_days_19 = day_data[(day_data['Date'] >= start_date_19) & (day_data['Date'] < target_dates['19-04-2024'])]
day_data_30_days_22 = day_data[(day_data['Date'] >= start_date_22) & (day_data['Date'] < target_dates['22-04-2024'])]

# Compute 30-day average volume for each stock for 19th and 22nd April
avg_volume_19 = day_data_30_days_19.groupby('Stock Name')['Volume'].mean()
avg_volume_22 = day_data_30_days_22.groupby('Stock Name')['Volume'].mean()

# Display the 30-day average volume for both dates
print("30-Day Average Volume for 19th April 2024:")
print(avg_volume_19)

print("\n30-Day Average Volume for 22nd April 2024:")
print(avg_volume_22)

# Define market open time
market_open_time = "09:15:00"

# Function to preprocess intraday data for analysis
def preprocess_intraday_data(df, target_date, avg_volume):
    df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df = df[df['Timestamp'] >= datetime.combine(target_date, datetime.strptime(market_open_time, "%H:%M:%S").time())]
    
    df = df.copy()
    df['Last Traded Quantity'] = df['Last Traded Quantity'].fillna(0)
    
    result = {}
    cumulative_volumes = {}
    
    for stock in df['Stock Name'].unique():
        stock_df = df[df['Stock Name'] == stock].copy()
        
        stock_df.set_index('Timestamp', inplace=True)
        stock_df['Cumulative Volume'] = stock_df['Last Traded Quantity'].rolling(window='60min').sum()
        
        crossover = stock_df[stock_df['Cumulative Volume'] > avg_volume.get(stock, float('inf'))]
        crossover_time = crossover.index[0] if not crossover.empty else None
        result[stock] = crossover_time
        
        cumulative_volumes[stock] = stock_df['Cumulative Volume']
    
    return result, cumulative_volumes

# Run the preprocessing function for both dates and corresponding average volumes
crossover_times_19, cumulative_volumes_19 = preprocess_intraday_data(intraday_data_19, target_dates['19-04-2024'], avg_volume_19)
crossover_times_22, cumulative_volumes_22 = preprocess_intraday_data(intraday_data_22, target_dates['22-04-2024'], avg_volume_22)

# Display the results
print("\nCrossover Times for 19th April 2024:", crossover_times_19)
print("\nCrossover Times for 22nd April 2024:", crossover_times_22)

# Print cumulative volumes
print("\nCumulative Volume for 19th April 2024:")
for stock, volume_series in cumulative_volumes_19.items():
    print(f"{stock}:")
    print(volume_series)

print("\nCumulative Volume for 22nd April 2024:")
for stock, volume_series in cumulative_volumes_22.items():
    print(f"{stock}:")
    print(volume_series)

# Plotting the cumulative volumes for 19th April
plt.figure(figsize=(14, 7))
for stock, volume_series in cumulative_volumes_19.items():
    plt.plot(volume_series.index, volume_series, label=stock)
plt.title('Cumulative Volume for 19th April 2024')
plt.xlabel('Time')
plt.ylabel('Cumulative Volume')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Plotting the cumulative volumes for 22nd April
plt.figure(figsize=(14, 7))
for stock, volume_series in cumulative_volumes_22.items():
    plt.plot(volume_series.index, volume_series, label=stock)
plt.title('Cumulative Volume for 22nd April 2024')
plt.xlabel('Time')
plt.ylabel('Cumulative Volume')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()























































































