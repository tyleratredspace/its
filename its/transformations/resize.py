from .base import BaseTransform
from PIL import Image


class ResizeTransform(BaseTransform):

    slug = "resize"

    def apply_transform(img, *args):

        size = [int(size_arg) for size_arg in args[0].split('x')]

        try:
            img.thumbnail(size, Image.ANTIALIAS)
        except Exception as e:
            raise e

        return img
