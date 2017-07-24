from pathlib import Path
from PIL import Image
from .base import BaseLoader
from ..errors import NotFoundError


class FileSystemLoader(BaseLoader):

    slug = "file_system"

    def load_image(namespace, filename):
        """
        Loads image from file system
        """
        # Path to the great grandparent directory of this file

        try:
            api_root = Path(__file__).parents[3]
            image_path = Path(api_root / namespace / filename)
            image = Image.open(image_path)
        except FileNotFoundError as e:
            raise NotFoundError(error="File Not Found at %s" % (image_path))

        return image
