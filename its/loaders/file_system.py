from .base import BaseLoader
from PIL import Image
from pathlib import Path

class FileSystemLoader(BaseLoader):

    slug = "file_system"

    def load_image(namespace, filename):
        """
        Loads image from file system
        """
        # Need some error handling here
        # Path to the great grandparent directory of this file
        api_root = Path(__file__).parents[3]
        image = Image.open(api_root / namespace / filename)

        return image
