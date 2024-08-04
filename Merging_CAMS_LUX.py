import pandas as pd
from datetime import datetime

def process_and_merge_datasets(soda_data_path, lux_values_path, output_path=None):
    # Load the datasets
    soda_data = pd.read_csv(soda_data_path)
    lux_values = pd.read_csv(lux_values_path)

    # Function to extract datetime from image name
    def extract_datetime_from_image_name(image_name):
        try:
            time, date_part_with_extension = image_name.split('_')
            date_part = date_part_with_extension.split('.')[:2]
            if len(time.split('.')) != 2 or len(date_part) != 2:
                raise ValueError("Unexpected format")

            datetime_str = f"{date_part[0]}.{date_part[1]}.2023 {time.replace('.', ':')}"
            return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
        except Exception as e:
            print(f"Error extracting datetime from image name {image_name}: {e}")
            return None

    # Apply the function to extract datetime
    lux_values['Timestamp'] = lux_values['Image Name'].apply(extract_datetime_from_image_name)

    # Convert the 'Time Period' column in soda_data to datetime
    soda_data['Time Period'] = pd.to_datetime(soda_data['Time Period'])

    # Assuming lux_values timestamps are in UTC+2
    lux_values['Timestamp'] = lux_values['Timestamp'].dt.tz_localize('Etc/GMT-2').dt.tz_convert('UTC')

    # Assuming soda_data timestamps are in UTC
    soda_data['Time Period'] = soda_data['Time Period'].dt.tz_localize('UTC')

    # Merge the datasets on the timestamps
    merged_data = pd.merge_asof(
        lux_values.sort_values('Timestamp'),
        soda_data.sort_values('Time Period'),
        left_on='Timestamp',
        right_on='Time Period',
        direction='nearest',
        tolerance=pd.Timedelta('1H')
    )

    # Display the merged dataset
    print("Merged Data (first 5 rows):")
    print(merged_data.head())

    # Save the merged dataset to a CSV file if output_path is provided
    if output_path:
        merged_data.to_csv(output_path, index=False)

    return merged_data

