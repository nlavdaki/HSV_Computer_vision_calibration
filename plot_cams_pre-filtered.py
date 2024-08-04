import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
import datetime
# Load the provided file
file_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\combined_Soda_data.csv'
df = pd.read_csv(file_path)


# Extract the time period before the "/"
df['Observation period'] = df['Observation period'].apply(lambda x: x.split('/')[0])

# Convert Observation period to datetime
df['Observation period'] = pd.to_datetime(df['Observation period'])

# Extract day and month for legend
df['Day_Month'] = df['Observation period'].dt.strftime('%m/%d')

# Extract time for x-axis
df['Time'] = df['Observation period'].dt.time

# Filter the data for the specified time range 02:00 to 20:00
df = df[(df['Observation period'].dt.time >= pd.to_datetime('02:00').time()) &
        (df['Observation period'].dt.time <= pd.to_datetime('20:00').time())]

# Convert time to datetime on a specific date
df['Datetime'] = df['Observation period'].apply(lambda x: x.replace(year=2020, month=1, day=1))

# Plot the data
plt.figure(figsize=(14, 7))

for label, df_group in df.groupby('Day_Month'):
    plt.plot(df_group['Datetime'], df_group['Clear sky GHI'], label=label)

plt.xlabel('Time of Day')
plt.ylabel('Clear Sky GHI (W/m²)')
plt.title('Clear Sky GHI by Time of Day - CAMS')
plt.legend(title='Day/Month 2023')

# Set the x-axis to hourly intervals
plt.gca().xaxis.set_major_locator(HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()


# # Load the CSV file
# file_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\final_soda_data.csv'  # Change this to the actual path of your CSV file
# df = pd.read_csv(file_path)
#
# # Convert "Time Period" to datetime
# df['Time Period'] = pd.to_datetime(df['Time Period'])
#
# # Extract time of day in hh:mm format and hour of day
# df['Time of Day'] = df['Time Period'].dt.strftime('%H:%M')
# df['Hour of Day'] = df['Time Period'].dt.hour + df['Time Period'].dt.minute / 60
#
# # Extract the date for the legend
# df['Date'] = df['Time Period'].dt.date
#
# # Plotting with dual x-axes, excluding numbers on the upper axis
# fig, ax1 = plt.subplots(figsize=(14, 8))
#
# # Plot with hour of day on primary x-axis
# for date, group in df.groupby('Date'):
#     ax1.plot(group['Hour of Day'], group['Clear Sky GHI'], marker='o', label=str(date))
#
# # Setting up the secondary x-axis
# ax2 = ax1.twiny()
# ax2.set_xlim(ax1.get_xlim())
# ax2.set_xticks([])  # Exclude numbers on the upper axis
# ax2.set_xticklabels([])
#
# # Labels and title
# ax1.set_xlabel('Hour of Day')
# ax1.set_ylabel('Clear Sky GHI')
# ax1.set_title('Clear Sky GHI vs Time of Day with Dual X-Axes')
# ax2.set_xlabel('Time of Day')
#
# # Legend and grid
# ax1.legend(title='Date')
# ax1.grid(True)
#
# plt.show()
