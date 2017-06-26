from .base import BaseTransform
from PIL import Image


class ResizeTransform(BaseTransform):

    def apply_transformation(img, *args):
        print(args)
        # img.resize()
        return img
