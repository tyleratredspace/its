from math import floor
from pathlib import Path
from PIL import Image
from .base import BaseTransform
from ..loaders import BaseLoader
from ..settings import OVERLAYS, OVERLAY_PLACEMENT, OVERLAY_LOADER
from ..errors import ITSTransformError

class OverlayTransform(BaseTransform):

    """
    Pastes a specified image over the input image.
    The overlay is placed according to the input expected position of its top left corner.
    Overlay placement arguments are percentages, with (0,0)
    representing the top left corner of the input image.
    See settings to change the default placement of the
    overlay when no position arguments are input.

    image.png?overlay=overlay_img_pathxPXxPY
    """
    slug = "overlay"

    def apply_transform(img, overlay, overlay_position=None):

        *overlay_position, overlay = overlay

        api_root = Path(__file__).parents[2]  # its/serverless-its
        its_root = Path(__file__).parents[1]  # its/
        loader = OverlayTransform.get_loader(OVERLAY_LOADER)

        if overlay.lower() not in OVERLAYS:
            namespace, *filename = overlay.split('/')
            filename = Path("/".join(filename))
            overlay_image = loader[0].load_image(namespace, filename)
        else:
            namespace, *filename = OVERLAYS[overlay.lower()].split('/')
            filename = Path("/".join(filename))
            overlay_image = loader[0].load_image(namespace, filename)

        # placement of top left corner of overlay
        if len(overlay_position) == 0:
            overlay_position = OVERLAY_PLACEMENT

        try:
            x_coord = floor((int(overlay_position[0]) / 100) * img.width)
            y_coord = floor((int(overlay_position[1]) / 100) * img.height)
        except ValueError as e:
            raise ITSTransformError(
                "Invalid arguments supplied to Overlay Transform." +
                "Overlay takes overlay_image_pathxPXxPY, where overlay_image_path is the path to the overlay image and " + 
                "(PX, PY) are optional percentage parameters indicating where the top left corner of the overlay should be placed."
            )

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

    def get_loader(OVERLAY_LOADER):
        
        loader_classes = BaseLoader.__subclasses__()

        loader = [
            loader for loader in loader_classes
            if loader.slug == OVERLAY_LOADER]

        if len(loader) == 1:
            return loader
        elif len(loader) == 0:
            raise ITSTransformError("Not Found Error: Overlay Image Loader with slug '%s' not found." %OVERLAY_LOADER)
        elif len(loader) > 1:
            raise ITSTransformError("Configuration Error: Two or more Image Loaders have slug '%s'." %OVERLAY_LOADER)
