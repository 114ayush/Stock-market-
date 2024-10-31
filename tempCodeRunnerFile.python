import pandas as pd
import mplfinance as mpf
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
def preprocess_intraday_data(df, target_date):
    df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df = df[df['Timestamp'] >= datetime.combine(target_date, datetime.strptime(market_open_time, "%H:%M:%S").time())]
    
    df['Last Traded Quantity'] = df['Last Traded Quantity'].fillna(0)
    
    # Set index to Timestamp for mplfinance
    df.set_index('Timestamp', inplace=True)
    
    # Ensure necessary columns for candlestick chart
    df = df[['Last Traded Quantity']].rename(columns={'Last Traded Quantity': 'Close'})
    df['Open'] = df['Close'].shift(1)  # Use previous close as open for next interval
    df['High'] = df[['Open', 'Close']].max(axis=1)  # High is max of open and close
    df['Low'] = df[['Open', 'Close']].min(axis=1)   # Low is min of open and close
    df.dropna(inplace=True)  # Remove any rows with NaN values

    return df

# Run the preprocessing function for both dates
candlestick_data_19 = preprocess_intraday_data(intraday_data_19, target_dates['19-04-2024'])
candlestick_data_22 = preprocess_intraday_data(intraday_data_22, target_dates['22-04-2024'])

# Plotting candlestick charts for 19th April
mpf.plot(candlestick_data_19, type='candle', volume=False, title='Candlestick Chart for 19th April 2024',
         style='charles', ylabel='Volume', figsize=(14, 7))

# Plotting candlestick charts for 22nd April
mpf.plot(candlestick_data_22, type='candle', volume=False, title='Candlestick Chart for 22nd April 2024',
         style='charles', ylabel='Volume', figsize=(14, 7))
