from .base import BaseTransform
from errors import ITSTransformError
from PIL import Image
from math import floor


class ResizeTransform(BaseTransform):

    slug = "resize"

    def apply_transform(img, resize_size):
        """
        Resizes input image while maintaining aspect ratio.
        """

        width, height = resize_size

        if img.width == 0 or img.height == 0:
            raise ITSTransformError(error="Input image cannot have zero width nor zero height.")
        else:
            ratio = img.width / img.height

        try:
            width = int(width) if width != '' else None
            height = int(height) if height != '' else None
        except ValueError as e:
            raise ITSTransformError(error="Resize takes WWxHH, WWx, or xHH, where WW is the requested width and HH is the requested height.")

        if width is None and height is None:
            raise ITSTransformError(error="Resize takes WWxHH, WWx, or xHH, where WW is the requested width and HH is the requested height.")

        if width is None and height:
            width = floor(ratio * height)

        if height is None:
            height = floor(ratio * width)

        img = img.resize([width, height], Image.ANTIALIAS)

        return img
