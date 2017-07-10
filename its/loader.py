"""
Script to validate images being submitted for transformation.
"""

from loaders import BaseLoader, FileSystemLoader
from errors import ITSLoaderError
import settings


def loader(namespace, filename):

    """
    Loads image using the IMAGE_LOADER specified in settings.
    """
    image = None

    loader_classes = BaseLoader.__subclasses__()

    image_loader = [loader 
        for loader in loader_classes 
        if loader.slug == settings.IMAGE_LOADER
    ]
    
    if len(image_loader) == 1:
        image = image_loader[0].load_image(namespace, filename)
    elif len(image_loader) == 0:
        raise ITSLoaderError(error="Not Found Error: Image loader not found.")
    elif len(image_loader) > 1:
        raise ITSLoaderError(error="Configuration Error: Two or more loaders have the same slug.")

    return image
