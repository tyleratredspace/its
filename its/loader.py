"""
Script to validate images being submitted for transformation.
"""

from loaders import BaseLoader


def loader(namespace, filename):

    """
    Cycles through the available loaders and
    attempts to load filename from namespace.
    if DEBUG=true, only uses FileSystemLoader
    """
    image = None
    loader_classes = BaseLoader.__subclasses__()

    for lclass in loader_classes:
        image = lclass.load_image(namespace, filename)

        if image:
            break

    return image
