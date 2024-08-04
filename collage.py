from datetime import datetime
import os
import glob
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for better handling of large images
import matplotlib.pyplot as plt
from matplotlib.image import imread
from collections import defaultdict

# Directory where images are stored
directory_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\raw\pngs\raw_pngs'
pattern = os.path.join(directory_path, '*.png')

# Function to parse datetime from image name
def parse_datetime_from_name(file_name):
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    time_part, date_part = base_name.split('_')
    hour, minute = map(int, time_part.split('.'))
    day, month = map(int, date_part.split('.'))
    return datetime(2023, month, day, hour, minute)

# Extract images and sort them by datetime
png_files = glob.glob(pattern)
png_files_sorted = sorted(png_files, key=lambda x: parse_datetime_from_name(x))

# Group images by day
images_by_day = defaultdict(list)
for file in png_files_sorted:
    day_key = parse_datetime_from_name(file).date()
    images_by_day[day_key].append(file)

# Determine grid size
max_images_per_day = max(len(images) for images in images_by_day.values())
n_days = len(images_by_day)

# Load one image to get its dimensions
sample_image = imread(png_files_sorted[0])
image_height, image_width, _ = sample_image.shape

# Calculate figure size based on the number of images and their dimensions
figsize = (max_images_per_day * (image_width / 200), n_days * (image_height / 200))

# Set DPI (lower value to avoid excessive size)
dpi = 300

# Plotting
fig, axs = plt.subplots(n_days, max_images_per_day, figsize=figsize, facecolor='white', dpi=dpi)
axs = axs.reshape(n_days, max_images_per_day)  # Ensure axs is always a 2D array

for day_idx, (day, images) in enumerate(images_by_day.items()):
    for hour_idx in range(max_images_per_day):
        ax = axs[day_idx, hour_idx]
        ax.set_facecolor('white')  # Set the face color of each subplot to white
        if hour_idx < len(images):
            file = images[hour_idx]
            img = imread(file)
            ax.imshow(img)
            base_name = os.path.splitext(os.path.basename(file))[0]
            ax.set_title('', fontsize=25, color='black')
        else:
            fig.delaxes(ax)  # Remove the empty subplot
        ax.axis('off')

# Adding titles above each image
for day_idx, (day, images) in enumerate(images_by_day.items()):
    for hour_idx in range(len(images)):
        ax = axs[day_idx, hour_idx]
        file = images[hour_idx]
        base_name = os.path.splitext(os.path.basename(file))[0]
        ax.text(0.5, 1.05, base_name, ha='center', va='bottom', transform=ax.transAxes, fontsize=25, color='black')

# Adjust subplots with reduced spacing
plt.subplots_adjust(wspace=0.1, hspace=0.5)

# Ensure the figure background is white
fig.patch.set_facecolor('white')

# Save the figure to a file
output_path = r'C:\Users\Nikos\Desktop\thesis\Paper\Data\collage_output.png'
plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)

print(f"Plot saved to {output_path}")
