from .base import BaseTransform
from PIL import Image
from flask import Flask, abort
from math import floor

class CropTransform(BaseTransform):

    slug = "crop"

    def apply_transform(img, *args):
        """
        Crops input img using 
        """

        center = [floor(img.size[0]/2), floor(img.size[1]/2)]

        try:
            cwidth = int(args[0].split('x')[0])
            cheight = int(args[0].split('x')[1])
        except Exception as e:
            abort(400)

        try:
            img = img.crop([center[0] - cwidth, center[1] - cheight, center[0] + cwidth, center[1] + cheight])
        except Exception as e:
            raise e

        img.show()
        return img
