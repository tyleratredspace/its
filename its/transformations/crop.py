from .base import BaseTransform
from errors import ITSTransformError
from PIL import Image
from math import floor
import re

class CropTransform(BaseTransform):

    slug = "crop"

    def apply_transform(img, crop_size, focal_point=None):
        """
        Crops input img about a focal point.
        The default focal point is the center of the image.
        
        crop : image.png?crop=WWxHH
        focal crop : image.png?crop=WWxHHxFXxFY
        smart crop : image_focus-FXxFY.png?crop=WWxHH
        """

        crop_width, crop_height, *focal_point = crop_size

        # no focal crop args, so check if focal args in filename
        if len(focal_point) == 0:
            # delims = '+^!'
            # filename = img.info['filename']
            # filename_focal = re.split(delims, filename)

            # if len(filename_focal) > 0: # smart crop
            #     focal_point = filename_focal
            # else: # default crop
            # default focal point is the center so 50% on the x and y axes 
            focal_point = [50, 50]

        # convert all arguments to ints since they're strings
        crop_width = int(crop_width)
        crop_height = int(crop_height)
        focal_x = int(focal_point[0])
        focal_y = int(focal_point[1])

        # make sure focal args are percentages
        if (focal_x < 0 or focal_x > 100) or (focal_y < 0 or focal_y > 100):
            error = ITSTransformError(error="Focus arguments should be between 0 and 100")
            result = error
        else:    
            focal_x = floor((focal_x / 100) * img.width)
            focal_y = floor((focal_y / 100) * img.height)

            try:
                result = img.crop([focal_x, focal_y, focal_x + crop_width, focal_y + crop_height])
            except ITSTransformError as e:
                result = img # return the original image since the transform failed
                e(error="Crop transform with requested size %sx%s and requested focal point [%s, %s] failed." %(crop_width, crop_height, focal_x, focal_y))
        
        img = result
        return img
