import pandas as pd
import matplotlib.pyplot as plt

# Load the merged dataset
merged_data = pd.read_csv(r'C:\Users\Nikos\Desktop\thesis\Paper\Data\merged_data.csv')

# Extract date information for grouping
merged_data['Day_Month'] = pd.to_datetime(merged_data['Timestamp']).dt.strftime('%m/%d')
merged_data['Hour'] = pd.to_datetime(merged_data['Timestamp']).dt.hour

# Filter the data for the specified time range 02:00 to 20:00 UTC
filtered_data = merged_data[(pd.to_datetime(merged_data['Timestamp']).dt.time >= pd.to_datetime('03:00').time()) &
                            (pd.to_datetime(merged_data['Timestamp']).dt.time <= pd.to_datetime('20:00').time())]


# Define a function to plot Lux Value and Clear Sky GHI for each day
def plot_day_data(day_month):
    day_data = filtered_data[filtered_data['Day_Month'] == day_month]

    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax2 = ax1.twinx()
    ax1.plot(day_data['Hour'], day_data['Clear Sky GHI'], 'g-', marker='o', label='Clear Sky GHI')
    ax2.plot(day_data['Hour'], day_data['Lux Value'], 'b-', marker='o', label='Lux Value')

    ax1.set_xlabel('Hour of Day', fontsize=25)
    ax1.set_ylabel('Clear Sky GHI (W/m²)', color='g', fontsize=25)
    ax2.set_ylabel('Lux Value (hsv)', color='b', fontsize=25)

    plt.title(f'Lux Value and Clear Sky GHI for {day_month}', fontsize=30)
    fig.tight_layout()
    plt.show()


# Plot the data for each unique day studied
unique_days = filtered_data['Day_Month'].unique()
for day in unique_days[:4]:  # Limit to 4 days for plotting
    plot_day_data(day)
