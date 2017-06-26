"""
Script to validate images being submitted for transformation.
"""

from loaders import BaseLoader, FileSystemLoader
import settings

def loader(namespace, filename):

    """
    Loads image using the DEFAULT_LOADER specified in settings.
    """
    image = None

    loader_classes = BaseLoader.__subclasses__()

    try:
        def_loader = [loader 
            for loader in loader_classes 
            if loader.loader_slug == settings.DEFAULT_LOADER
        ]
    except Exception as e:
        raise e
   
    image = def_loader[0].load_image(namespace, filename)

    return image
