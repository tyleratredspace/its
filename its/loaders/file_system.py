from .base import BaseLoader
from PIL import Image
from pathlib import Path

class FileSystemLoader(BaseLoader):

    def load_image(namespace, filename):
        """
        Loads image from file system
        """

        its_root = Path(__file__).parents[3]
        image = Image.open(its_root/namespace/filename)

        return image





