from io import BytesIO

import requests
from PIL import Image

from ..errors import NotFoundError
from ..settings import NAMESPACES
from .base import BaseLoader


class HTTPLoader(BaseLoader):

    slug = "http"
    parameter_name = "prefixes"

    @staticmethod
    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        prefixes = set(
            filename.rsplit("/", 1)[0].split("/")
        )  # everything before the final slash
        params = NAMESPACES[namespace][HTTPLoader.parameter_name]
        intersect = set(params).intersection(prefixes)

        if len(intersect) > 0:
            # create an empty bytes object to store the image bytes in
            file_obj = BytesIO(requests.get(filename).content)
        else:
            raise NotFoundError("Namespace {} is not configured.".format(namespace))

        return file_obj

    @staticmethod
    def load_image(namespace, filename):
        """
        Loads image from http.
        """
        try:
            file_obj = HTTPLoader.get_fileobj(namespace, filename)
            img = Image.open(file_obj)

        except NotFoundError as e:
            raise NotFoundError("An error occurred: '%s'" % str(e))

        return img
