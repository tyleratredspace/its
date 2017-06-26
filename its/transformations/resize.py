from .base import BaseTransform
from PIL import Image
from math import floor
from flask import Flask, abort


class ResizeTransform(BaseTransform):

    slug = "resize"

    def apply_transform(img, *args):
        """
        Resizes input image while maintaining aspect ratio.
        """

        try:
            rwidth= args[0].split('x')[0]
            rheight = args[0].split('x')[1]
            size_ratio = img.size[0] / img.size[1]
        except Exception as e:
            # print("Resize takes WWxHH, WWx, or xHH, where WW is the requested width and HH is the requested height.")
            abort(400)

        try:
            if rwidth != '' and rheight != '':
                rwidth = int(rwidth)
                rheight = int(rheight)
            elif rwidth == '' and rheight != '':
                rheight = int(rheight)
                rwidth = floor(size_ratio * rheight)
            elif rheight == '' and rwidth != '':
                rwidth = int(rwidth)
                rheight = floor(size_ratio * rwidth)
        except Exception as e:
            abort(400)
        
        try:
            img.thumbnail([rwidth,rheight], Image.ANTIALIAS)
        except Exception as e:
            abort(304)

        return img
