from .base import BaseTransform
from PIL import Image
from flask import Flask, abort
from math import floor

class CropTransform(BaseTransform):

    slug = "crop"

    def apply_transform(img, *args):
        """
        Crops input img about a focal point.
        The default focal point is the center of the image.
        """
        crop_args = args[0].split('x')
        try:
            crop_size = [int(crop_args[0]), int(crop_args[1])]

            if len(crop_args) == 2:
                focal = [floor(img.size[0]/2), floor(img.size[1]/2)]
            else:
                focal = [int(crop_args[2]), int(crop_args[3])]
        except Exception as e:
            abort(400)

        try:

            if len(crop_args) == 2:
                img = img.crop([focal[0] - crop_size[0], focal[1] - crop_size[1], focal[0] + crop_size[0], focal[1] + crop_size[1]])
            else:
                img = img.crop([focal[0], focal[1], focal[0] + crop_size[0], focal[1] + crop_size[1]])
            
        except Exception as e:
            abort(304)

        return img
