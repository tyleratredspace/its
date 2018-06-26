"""
Script to validate images being submitted for transformation.
"""

from flask import request

from .errors import ConfigError, ITSLoaderError
from .loaders import BaseLoader
from .settings import NAMESPACES


def loader(namespace, filename):

    """
    Loads image using the IMAGE_LOADER specified in settings.
    """
    image = None

    loader_classes = BaseLoader.__subclasses__()

    if namespace in NAMESPACES:
        loader_parameters = NAMESPACES[namespace]
        loader_slug = loader_parameters["loader"]

        image_loader = [
            loader for loader in loader_classes if loader.slug == loader_slug
        ]

        if len(image_loader) == 1:
            # handle self-referential http backend use.
            # if we get a request like /my_http_backend/image.example.com/test/image.jpg, we want to
            # serve as if we got `/test/image.jpg`
            path_segments = filename.split("/")
            if image_loader[0].slug == "http" and path_segments[0] == request.host:
                namespace = path_segments[1]
                filename = "/".join(path_segments[2:])
                return loader(namespace, filename)
            elif filename.endswith(".svg"):
                image = image_loader[0].get_fileobj(namespace, filename)
            else:
                image = image_loader[0].load_image(namespace, filename)
        elif not image_loader:
            raise ITSLoaderError("No Image Loader with slug '%s' found." % loader_slug)
        elif len(image_loader) > 1:
            raise ConfigError("Two or more Image Loaders have slug '%s'." % loader_slug)
    else:
        raise ConfigError("No Backend for namespace '%s'." % namespace)

    return image
