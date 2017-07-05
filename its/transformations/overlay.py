from .base import BaseTransform
from PIL import Image
from math import floor
from pathlib import Path
from settings import OVERLAYS


class OverlayTransform(BaseTransform):

    """
    Pastes a specified image over the input image.
    The overlay is placed according to the input expected position of its top left corner.
    Overlay placement arguments are percentages, with (0,0) representing the top left corner of the input image.
    See settings to change the default placement of the overlay when no position arguments are input.

    image.png?overlay=overlay_img.pngxPXxPY
    """
    slug = "overlay"

    def apply_transform(img, overlay, overlay_position=None):

        # overlay args should be split in pipeline instead
        overlay = overlay.split('x')
        overlay, *overlay_position = overlay

        api_root = Path(__file__).parents[2]
        its_root = Path(__file__).parents[1]

        if overlay.lower() not in OVERLAYS.keys():
            overlay_image = Image.open(Path(api_root / overlay))
        else:
            overlay_image = Image.open(its_root / OVERLAYS[overlay.lower()])

        # placement of top left corner of overlay
        if len(overlay_position) != 0:
            x_coord = floor((int(overlay_position[0]) / 100) * img.width)
            y_coord = floor((int(overlay_position[1]) / 100) * img.height)
        # else: # default placement

        # Only the overlay has an alpha channel
        if(img.mode != "RGBA"):
            new_img = img.copy()
        else:
            # overlay and input img have alpha channels
            # make an image the size of the background with 
            # RGBA mode and alpha composite new image with background
            # this maintains the alpha channel of the background
            new_img = Image.new("RGBA", img.size)
            new_img = Image.alpha_composite(new_img, img)

        new_img.paste(overlay_image, box=[x_coord, y_coord], mask=overlay_image)

        img = new_img
        return img
