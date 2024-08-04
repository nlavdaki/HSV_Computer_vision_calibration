from Cropping_images import crop_and_save_images
from Lux_extraction import lux_extract
from CAMS_preproc60_Filter import combine_soda_data, generate_final_csv
from plot_lux_values import plot_lux_values
from Merging_CAMS_LUX import process_and_merge_datasets
import os

# Define the source and destination directories
images_for_cropping_dir = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\raw\pngs\raw_pngs'
destination_dir_for_cropped = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\raw\pngs\cropped_pngs'
# Define the output CSV file path
lux_output_csv_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\lux_values.csv'
source_soda_raw_directory = r'C:\Users\Nikos\Desktop\thesis\soda_data\raw'
Data_destination_directory = r'C:\Users\Nikos\Desktop\thesis\Paper\Data'


# #1 Image cropping
# crop_and_save_images(images_for_cropping_dir, destination_dir_for_cropped, cropx=80, cropy=80, offsetx=-60, offsety=-180)

#2 Lux CV extraction
lux_extract(destination_dir_for_cropped, lux_output_csv_path)

print('Lux Dataset Created at', lux_output_csv_path)

#3 plot Lux and cams
#plot_lux_values(lux_output_csv_path)
#cams filtered

#4 Merge all soda data into 1 & filter
try:
    combined_file = combine_soda_data(source_soda_raw_directory, Data_destination_directory)
    print(f"Combined file created successfully at: {combined_file}")
except Exception as e:
    print(f"Error combining data: {e}")
    combined_file = None

if combined_file and os.path.exists(combined_file):
    lux_values_csv_path = os.path.join(Data_destination_directory, 'lux_values.csv')
    final_csv_path = os.path.join(Data_destination_directory, 'final_soda_data.csv')

    try:
        generate_final_csv(combined_file, lux_values_csv_path, final_csv_path)
        print(f"Final data saved to: {final_csv_path}")
    except Exception as e:
        print(f"Error generating final CSV: {e}")
else:
    print("Combined file was not created. Exiting.")

#5 Merge all datasets
merged_data = process_and_merge_datasets(
    soda_data_path= final_csv_path,
    lux_values_path= lux_values_csv_path,
    output_path= r'C:\Users\Nikos\Desktop\thesis\Paper\Data\merged_data.csv')

#6 Scatter and ther plots
