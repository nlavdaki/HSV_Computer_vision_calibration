import pandas as pd
import matplotlib.pyplot as plt


def plot_lux_values(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Split the 'Image Name' column into 'Time' and 'Date'
    df[['Time', 'Date']] = df['Image Name'].str.split('_', expand=True)
    df['Time'] = df['Time'].str.replace('.', ':')
    df['Date'] = df['Date'].str.replace('.png', '')

    # Remove any anomalies in 'Time' column
    df = df[df['Time'] != 'adjusted']

    # Convert 'Time' to proper datetime format and standardize the date
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').apply(lambda x: x.replace(year=1900, month=1, day=1))

    # Convert 'Date' to proper datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')

    # Set the plot size
    plt.figure(figsize=(12, 8))

    # Group the data by 'Date' and plot each group
    for date, group in df.groupby('Date'):
        plt.plot(group['Time'], group['Lux Value'], marker='o', label=date.strftime('%d.%m'))

    # Set plot title and labels
    plt.title('DT Synthetic Values-Lux by Time of Day')
    plt.xlabel('Time of Day')
    plt.ylabel('Lux (lumen)')
    plt.legend(title='Date (dd.mm)')
    plt.xticks(rotation=45)

    # Format the x-axis to show time of day in HH:MM format
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=1))

    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

lux_output_csv_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\lux_values.csv'

plot_lux_values(lux_output_csv_path)