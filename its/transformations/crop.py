from .base import BaseTransform
from PIL import Image
<<<<<<< HEAD
=======
from flask import Flask, abort
>>>>>>> 6e8a35dd6fd04b26f059e764538c3f9721415a50
from math import floor

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
        crop_x, crop_y = crop_size.split('x')
        
        # smart crop
        if len(args) == 2 and len(crop_args) == 2:
            filename = args[1][0]
            fname_split = filename.find("focus-")
            fname_args = filename[fname_split + len("focus-"):].split('_')
            fname_args[1] = fname_args[1].split(".")[0]
            crop_args[2:3] = [fname_args[0], fname_args[1]]

        try:
            crop_size = [int(crop_args[0]), int(crop_args[1])]

            if len(crop_args) == 2:
                focal = [floor(img.size[0]/2), floor(img.size[1]/2)]
            else:  # focal crop
                focal = [int(crop_args[2]), int(crop_args[3])]
                # smart and focal should take in percentages
                if focal[0] < 0 or focal[0] > 100:
                    print("Focus arguments should be between 0 and 100")
                    abort(400)
                elif focal[1] < 0 or focal[1] > 100:
                    print("Focus arguments should be between 0 and 100")
                    abort(400)
                focal[0] = floor((focal[0]/100) * img.size[0])
                focal[1] = floor((focal[1]/100) * img.size[1])
        except Exception as e:
            print(e)
            abort(400)

        try:

            if len(crop_args) == 2: # regular crop
                img = img.crop([focal[0] - crop_size[0], focal[1] - crop_size[1], focal[0] + crop_size[0], focal[1] + crop_size[1]])
            else: # smart crop and focal crop

                img = img.crop([focal[0], focal[1], focal[0] + crop_size[0], focal[1] + crop_size[1]])
        except Exception as e:
            print(e)
            abort(400)

        return img
