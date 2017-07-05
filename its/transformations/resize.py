from .base import BaseTransform
from PIL import Image
from math import floor


class ResizeTransform(BaseTransform):

    slug = "resize"

    def apply_transform(img, resize_size):
        """
        Resizes input image while maintaining aspect ratio.
        """

        try:
            width, height = resize_size.split('x')
            ratio = img.width / img.height
        except (ZeroDivisionError, ValueError) as e:
            print("Resize takes WWxHH, WWx, or xHH, where WW is the requested width and HH is the requested height.")

        # converts arguments to ints and calculates
        # rwdith/riheight if missing an argument
        if width != '' and height != '':
            width = int(width)
            height = int(height)
        elif width == '' and height != '':
            height = int(height)
            width = floor(ratio * height)
        elif height == '' and width != '':
            width = int(width)
            height = floor(ratio * width)

        try:
            img = img.resize([width,height], Image.ANTIALIAS)
        except Exception as e:
            print("Failed to resize image.")

        return img
