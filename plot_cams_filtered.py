import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
import datetime

# Load the provided file
file_path = r"C:\Users\Nikos\Desktop\thesis\Paper\Data\final_soda_data.csv"
df = pd.read_csv(file_path)

# Convert Time Period to datetime
df['Time Period'] = pd.to_datetime(df['Time Period'])

# Extract day and month for legend
df['Day_Month'] = df['Time Period'].dt.strftime('%m/%d')

# Extract time for x-axis
df['Time'] = df['Time Period'].dt.time

# Filter the data for the specified time range 02:00 to 20:00
df = df[(df['Time Period'].dt.time >= pd.to_datetime('02:00').time()) &
        (df['Time Period'].dt.time <= pd.to_datetime('20:00').time())]

# Convert time to datetime on a specific date
df['Datetime'] = df['Time Period'].apply(lambda x: x.replace(year=2023, month=1, day=1))

# Plot the data
plt.figure(figsize=(14, 7))

for label, df_group in df.groupby('Day_Month'):
    plt.plot(df_group['Datetime'], df_group['Clear Sky GHI'], marker='o', label=label)

plt.xlabel('Time of Day')
plt.ylabel('Clear Sky GHI')
plt.title('Clear Sky GHI by Time of Day for Different Dates')
plt.legend(title='Day and Month')

# Set the x-axis to hourly intervals
plt.gca().xaxis.set_major_locator(HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()
