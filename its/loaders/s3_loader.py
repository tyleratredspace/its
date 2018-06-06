from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from PIL import Image

from ..errors import NotFoundError
from ..settings import NAMESPACES
from .base import BaseLoader


class S3Loader(BaseLoader):

    slug = "s3"
    parameter_name = "bucket"

    @staticmethod
    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        # get the s3 resource
        s3 = boto3.resource("s3")

        bucket = s3.Bucket(NAMESPACES[namespace][S3Loader.parameter_name])

        # create an empty bytes object to store the image bytes in
        file_obj = BytesIO()
        bucket.download_fileobj(filename, file_obj)

        return file_obj

    @staticmethod
    def load_image(namespace, filename):
        """
        Loads image from AWS S3 bucket.
        """
        try:
            file_obj = S3Loader.get_fileobj(namespace, filename)
            image = Image.open(file_obj)

        except ClientError as e:
            raise NotFoundError("An error occurred: '%s'" % str(e))

        return image
