import os
import pandas as pd
from datetime import datetime, timedelta

def combine_soda_data(source_soda_raw_directory, Data_destination_directory, combined_filename='combined_Soda_data.csv'):
    """
    Combine multiple .txt files from the source directory into a single CSV file in the destination directory.

    Parameters:
    source_directory (str): Path to the directory containing the .txt files.
    destination_directory (str): Path to the directory where the combined CSV file will be saved.
    combined_filename (str): Name of the combined CSV file. Defaults to 'combined_Soda_data.csv'.
    """
    if not os.path.exists(Data_destination_directory):
        os.makedirs(Data_destination_directory)

    combined_df = pd.DataFrame()

    for filename in os.listdir(source_soda_raw_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(source_soda_raw_directory, filename)
            df = pd.read_csv(file_path, sep=';', usecols=['Observation period', 'Clear sky GHI'])
            df['Clear sky GHI'] *= 60
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_csv_path = os.path.join(Data_destination_directory, combined_filename)
    combined_df.to_csv(combined_csv_path, index=False)

    if os.path.exists(combined_csv_path) and not combined_df.empty:
        return combined_csv_path
    else:
        raise FileNotFoundError(f"Failed to create the combined CSV file at {combined_csv_path}")

def adjust_for_athens_timezone(image_name):
    try:
        time_part, date_part_with_extension = image_name.split('_')
        date_part = date_part_with_extension.split('.')[0:2]
        if len(time_part.split('.')) != 2 or len(date_part) != 2:
            raise ValueError("Unexpected format")

        hour, minute = map(int, time_part.split('.'))
        day, month = map(int, date_part)
        hour -= 2

        adjusted_datetime = datetime(2023, month, day, hour, minute)
        if adjusted_datetime.hour >= 24:
            adjusted_datetime += timedelta(hours=-24)
            adjusted_datetime += timedelta(days=1)

        return adjusted_datetime
    except Exception as e:
        print(f"Error adjusting for Athens timezone for image name {image_name}: {e}")
        return None

def extract_datetime_from_image_name(image_name):
    try:
        time, date_part_with_extension = image_name.split('_')
        date_part = date_part_with_extension.split('.')[0:2]
        if len(time.split('.')) != 2 or len(date_part) != 2:
            raise ValueError("Unexpected format")

        datetime_str = f"{date_part[0]}.{date_part[1]}.2023 {time.replace('.', ':')}"
        return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
    except Exception as e:
        print(f"Error extracting datetime from image name {image_name}: {e}")
        return None

def generate_final_csv(combined_csv_path, lux_values_csv_path, final_csv_path):
    combined_df = pd.read_csv(combined_csv_path)
    lux_values_df = pd.read_csv(lux_values_csv_path)

    print("Combined DataFrame:")
    print(combined_df.head())

    print("Lux Values DataFrame:")
    print(lux_values_df.head())

    # Create a dictionary to map image names to adjusted observation periods
    image_name_to_period = {}
    for image_name in lux_values_df['Image Name']:
        adjusted_datetime = adjust_for_athens_timezone(image_name)
        if adjusted_datetime:
            image_name_to_period[image_name] = adjusted_datetime

    print("Image Name to Period Mapping:")
    for key, value in image_name_to_period.items():
        print(f"{key}: {value}")

    final_data = []

    for index, row in lux_values_df.iterrows():
        image_name = row['Image Name']
        if image_name in image_name_to_period:
            datetime_obj = image_name_to_period[image_name]
            # Matching logic for observation period
            combined_df['Start Time'] = combined_df['Observation period'].apply(lambda x: x.split('/')[0])
            matching_row = combined_df[combined_df['Start Time'] == datetime_obj.isoformat(timespec='seconds') + ".0"]
            if not matching_row.empty:
                ghi_value = matching_row.iloc[0]['Clear sky GHI']
            else:
                ghi_value = 0
            final_data.append([datetime_obj, ghi_value])

    print("Final Data Collected:")
    for row in final_data:
        print(row)

    final_df = pd.DataFrame(final_data, columns=['Time Period', 'Clear Sky GHI'])
    final_df.to_csv(final_csv_path, index=False)