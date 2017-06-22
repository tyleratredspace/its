from .base import BaseLoader
from PIL import Image


class FileSystemLoader(BaseLoader):

    def load_image(namespace, filename):
        """
        Loads image from file system
        """
        image = Image.open(namespace + "/" + filename)

        return image
