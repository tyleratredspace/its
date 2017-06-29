from .base import BaseTransform
from PIL import Image
from math import floor
from pathlib import Path


class OverlayTransform(BaseTransform):

    """
    Generic image transform type class
    """
    slug = "overlay"

    def apply_transform(img, *args):

        overlay_args = args[0].split('x')
        api_root = Path(__file__).parents[2]
        its_root = Path(__file__).parents[1]

        if overlay_args[2].lower() != "passport":
            if overlay_args[2].find('^') > 0:
                overlay = overlay_args[2].split('^')
                if overlay[0][0] == "/":
                    overlay[0][0] = " "
                    overlay[0].lstrip()

                overlay_image = Image.open(Path(api_root / overlay[0]))
                # check in cache for a version of overlay
                # that has already been transformed
                # do the temporary transforms on the overlay
            else:
                overlay_image = Image.open(Path(api_root / overlay_args[2]))
        else:
            overlay_image = Image.open(
                                        its_root /
                                        "static/Passport_Compass_Rose.png"
                                    )

        # placement of top left corner of overlay
        x_coord = floor((int(overlay_args[0]) / 100) * img.width)
        y_coord = floor((int(overlay_args[1]) / 100) * img.height)

        # Only the overlay has an alpha channel
        if(img.mode != "RGBA"):
            new_img = img.copy()
        else:
            # overlay and input img have alpha channels
            new_img = Image.new("RGBA", img.size)
            new_img = Image.alpha_composite(new_img, img)

        new_img.paste(overlay_image, box=[x_coord, y_coord], mask=overlay_image)

        img = new_img

        return img
