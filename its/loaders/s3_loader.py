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
        s3_resource = boto3.resource("s3")

        bucket_name = NAMESPACES[namespace][S3Loader.parameter_name]
        key = "{namespace}/{filename}".format(namespace=namespace, filename=filename)
        s3_object = s3_resource.Object(bucket_name=bucket_name, key=key)

        # create an empty bytes object to store the image bytes in
        file_obj = BytesIO()
        s3_object.download_fileobj(file_obj)

        return file_obj

    @staticmethod
    def load_image(namespace, filename):
        """
        Loads image from AWS S3 bucket.
        """
        try:
            file_obj = S3Loader.get_fileobj(namespace, filename)
        except ClientError as error:
            error_code = error.response["Error"]["Code"]

            if error_code == '404':
                raise NotFoundError("An error occurred: '%s'" % str(error))

            raise error

        image = Image.open(file_obj)

        return image
