from math import floor
from PIL import Image
from .base import BaseTransform
from ..errors import ITSTransformError


class ResizeTransform(BaseTransform):

    slug = "resize"

    def apply_transform(img, resize_size):
        """
        Resizes input image while maintaining aspect ratio.
        """

        width, height = resize_size

        if img.width == 0 or img.height == 0:
            raise ITSTransformError(
                "Invalid arguments supplied to Resize Transform." +
                "Input image cannot have zero width nor zero height."
                )

        try:
            width = int(width) if width != '' else None
            height = int(height) if height != '' else None
        except ValueError as e:
            raise ITSTransformError(
                "Invalid arguments supplied to Resize Transform." +
                "Resize takes WWxHH, WWx, or xHH," +
                " where WW is the requested width and HH is the requested height. Both must be integers."
                )

        if width is None and height is None:
            raise ITSTransformError(
                "Invalid arguments supplied to Resize Transform." +
                "Resize takes WWxHH, WWx, or xHH," +
                " where WW is the requested width and HH is the requested height. Both must be integers."
                )

        if width is None and height:
            width = floor((img.height / img.width) * height)

        if height is None:
            height = floor((img.width / img.height) * width)

        # width and height are the max width and max height expected
        # calculate a resize ratio between them and the original sizes

        ratio = min(width / img.width, height / img.height)
        img = img.resize([floor(img.width * ratio), floor(img.height * ratio)], Image.ANTIALIAS)

        return img
