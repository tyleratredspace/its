import re
from PIL import Image, ImageOps
from math import floor
from .base import BaseTransform
from ..errors import ITSTransformError
from ..settings import DELIMITERS_RE, FOCUS_KEYWORD


class FitTransform(BaseTransform):

    slug = "crop"

    @staticmethod
    def apply_transform(img, crop_size, focal_point=None):
        """
        Crops input img about a focal point.
        The default focal point is the center of the image.

        crop : image.png?crop=WWxHH
        focal crop : image.png?crop=WWxHHxFXxFY
        smart crop : image_focus-FXxFY.png?crop=WWxHH
        """

        crop_width, crop_height, *focal_point = crop_size
        filename = img.info['filename']
        # match everything before and including the keyword
        pre_keyword_pattern = '.+?(' + FOCUS_KEYWORD + ')'
        # match the file type and period in the filename
        file_ext_patten = '(\.).+'

        if len(focal_point) == 0:
            # if FOCUS_KEYWORD is present in filename, do smart crop
            if filename.find(FOCUS_KEYWORD) >= 0:  # smart crop
                # Match and remove the non-argument filename parts using the patterns defined above
                filename = re.sub(pre_keyword_pattern, '', filename, flags=re.IGNORECASE)
                filename = re.sub(file_ext_patten, '', filename, flags=re.IGNORECASE)
                filename_focal = re.split(DELIMITERS_RE, filename)
                focal_point = filename_focal
            else:  # default crop, focal point is the center so 50% on the x & y axes
                focal_point = [50, 50]

        # convert all arguments to ints since they're strings
        crop_width = int(crop_width)
        crop_height = int(crop_height)
        focal_x = int(focal_point[0])
        focal_y = int(focal_point[1])

        if (focal_x < 0 or focal_x > 100) or (focal_y < 0 or focal_y > 100):
            # make sure focal args are percentages
            raise ITSTransformError(error="Focus arguments should be between 0 and 100")
        else:
            try:

                img = ImageOps.fit(img, (crop_width, crop_height), Image.ANTIALIAS, centering=(focal_x, focal_y))

            except ITSTransformError as e:
                raise e(
                        error="Crop transform with requested size %sx%s" +
                        "and requested focal point [%s, %s] failed."
                        % (crop_width, crop_height, focal_x, focal_y))

        return img
