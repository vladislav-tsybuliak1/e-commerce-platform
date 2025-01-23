import os

from PIL import Image


def resize_image(temp_path: str, file_path: str, max_file_size: int) -> None:
    current_size = os.path.getsize(temp_path)

    print("current_size = ", current_size)

    if current_size > max_file_size:
        with Image.open(temp_path) as img:
            width, height = img.size

            scaling_factor = (max_file_size / current_size) ** 0.5
            new_width = int(width * scaling_factor)
            new_height = int(height * scaling_factor)
            resized_img = img.resize((new_width, new_height))
            resized_img.save(file_path)
            print("new_size = ", resized_img.size)

    else:
        os.rename(temp_path, file_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)
