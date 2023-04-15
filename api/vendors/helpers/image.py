from PIL import Image
from typing import Tuple


def get_new_image_dimensions(original_dimensions, new_width: int):
    original_width, original_height = original_dimensions

    if original_width < new_width:
        return original_dimensions
    
    aspect_ratio = original_height / original_width
    new_height = round(new_width * aspect_ratio)

    return (new_width, new_height)


def resize_image(img_path, width: int):
    if img_path:
        with Image.open(img_path) as image:
            new_size = get_new_image_dimensions(image.size, width)
            if new_size == image.size:
                return

            return image.resize(new_size, Image.ANTIALIAS)