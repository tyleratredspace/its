from .base import BaseLoader
from errors import NotFoundError
from PIL import Image
from pathlib import Path


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
            raise NotFoundError(error="File Not Found at %s"%(image_path))


        return image
