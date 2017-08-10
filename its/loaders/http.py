from .base import BaseLoader
from ..errors import NotFoundError
from PIL import Image
from io import BytesIO
import re
from ..settings import BACKENDS
import urllib.request

class HTTPLoader(BaseLoader):

    slug = "http"
    parameter_name = "prefixes"

    @staticmethod
    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        prefixes = set(filename.rsplit('/', 1)[0].split('/')) # everything before the final slash
        params = BACKENDS[namespace][HTTPLoader.parameter_name]
        intersect = list(set(params).intersection(prefixes))
        if len(intersect) > 0:
            local_filename, headers = urllib.request.urlretrieve(filename)
        else:
            raise NotFoundError("Namespace {} is not configured.".format(namespace))

        # create an empty bytes object to store the image bytes in
        with open(local_filename) as file_obj:
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

        return image
