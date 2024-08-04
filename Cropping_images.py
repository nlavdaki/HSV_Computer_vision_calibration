import os
import cv2

# Function to crop the central region of the image
def crop_center(img, cropx, cropy, offsetx, offsety):
    y, x, _ = img.shape
    startx = (x // 2) - (cropx // 2) - offsetx
    starty = (y // 2) - (cropy // 2) - offsety
    # Ensure that startx and starty are not negative
    startx = max(startx, 0)
    starty = max(starty, 0)
    return img[starty:starty + cropy, startx:startx + cropx]


def crop_center(img, cropx, cropy, offsetx, offsety):
    """
    Crops the central region of the image with specified offsets.

    Parameters:
        img (numpy.ndarray): The image to crop.
        cropx (int): The width of the cropped image.
        cropy (int): The height of the cropped image.
        offsetx (int): The horizontal offset from the center.
        offsety (int): The vertical offset from the center.

    Returns:
        numpy.ndarray: The cropped image.
    """
    y, x, _ = img.shape
    startx = (x // 2) - (cropx // 2) - offsetx
    starty = (y // 2) - (cropy // 2) - offsety
    # Ensure that startx and starty are not negative
    startx = max(startx, 0)
    starty = max(starty, 0)
    return img[starty:starty + cropy, startx:startx + cropx]


def create_directory_if_not_exists(directory):
    """
    Creates the directory if it does not exist.

    Parameters:
        directory (str): The directory path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def crop_and_save_images(source_dir, destination_dir, cropx, cropy, offsetx, offsety):
    """
    Crops images from the source directory and saves them to the destination directory.

    Parameters:
        source_dir (str): The source directory containing images.
        destination_dir (str): The destination directory for cropped images.
        cropx (int): The width of the cropped image.
        cropy (int): The height of the cropped image.
        offsetx (int): The horizontal offset from the center.
        offsety (int): The vertical offset from the center.
    """
    create_directory_if_not_exists(destination_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".png"):
            img_path = os.path.join(source_dir, filename)
            img = cv2.imread(img_path)

            cropped_img = crop_center(img, cropx, cropy, offsetx, offsety)

            cv2.imwrite(os.path.join(destination_dir, filename), cropped_img)

    print("Cropping and saving of images completed at", destination_dir)

crop_and_save_images(r'C:\Users\Nikos\Documents\Kit\shared\screenshots', r'C:\Users\Nikos\Documents\Kit\shared\screenshots\paper_dataset_2', cropx=45, cropy=45, offsetx=20, offsety=-120)
