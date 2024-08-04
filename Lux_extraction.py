import cv2
import numpy as np
import os
import pandas as pd

# Function to extract the average lux value from an image
def extract_lux_value(image_path):
    # Function to map HSV values to lux values based on the provided legend
    def hsv_to_lux(h, s, v):
        if v < 50:  # Very dark colors are considered black, mapped to 0 lux
            return 0

        # Reversed and adjusted Mapping HSV values to Lux values based on the color legend
        if 0 <= h <= 15:  # Red
            return 35000  # Highest lux value for low hues (red)
        elif 15 < h <= 30:  # Orange
            return 30000 + ((30 - h) / 18.0) * 5000  # 30000 to 35000 lux
        elif 30 < h <= 45:  # Yellow
            return 25000 + ((45 - h) / 24.0) * 5000  # 25000 to 30000 lux
        elif 45 < h <= 60:  # Light Green
            return 20000 + ((60 - h) / 14.0) * 5000  # 20000 to 25000 lux
        elif 60 < h <= 90:  # Green
            return 15000 + ((90 - h) / 27.0) * 5000  # 15000 to 20000 lux
        elif 90 < h <= 120:  # Blue
            return 10000 + ((120 - h) / 30.0) * 5000  # 10000 to 15000 lux
        elif 120 < h <= 180:  # Light Blue
            return 5000 + ((180 - h) / 60.0) * 5000  # 5000 to 10000 lux
        elif 180 < h <= 240:  # Dark Blue
            return 1000 + ((240 - h) / 60.0) * 4000  # 1000 to 5000 lux
        else:
            return 0

    image = cv2.imread(image_path)

    if image is not None:
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Calculate the lux value for each pixel and then the mean lux value for the image
        lux_values = np.array([hsv_to_lux(h, s, v) for h, s, v in hsv_image.reshape(-1, 3)])
        mean_lux_value = np.mean(lux_values)
        return mean_lux_value
    else:
        return None

# Main script
# Main script
def lux_extract(destination_dir_for_cropped, lux_output_csv_path):
    # Initialize a list to store the results
    results = []

    # Iterate through each image in the directory
    for filename in os.listdir(destination_dir_for_cropped):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust the file extensions if necessary
            image_path = os.path.join(destination_dir_for_cropped, filename)
            lux_value = extract_lux_value(image_path)
            if lux_value is not None:
                results.append([filename, lux_value])

    # Create a DataFrame from the results
    df = pd.DataFrame(results, columns=['Image Name', 'Lux Value'])

    # Normalize the Lux values to start from 0
    min_lux_value = df['Lux Value'].min()
    df['Lux Value'] = df['Lux Value'] - min_lux_value

    # Save the DataFrame to a CSV file
    df.to_csv(lux_output_csv_path, index=False)

    print('Lux Dataset Created at', lux_output_csv_path)