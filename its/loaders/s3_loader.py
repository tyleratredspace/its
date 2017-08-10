from .base import BaseLoader
from ..errors import NotFoundError
from PIL import Image
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from ..settings import BACKENDS


class S3Loader(BaseLoader):

    slug = "s3"
    parameter_name = "buckets"

    @staticmethod
    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename,
        returns a file-like or bytes-like object.
        """
        # get the s3 resource
        s3 = boto3.resource('s3')

        bucket_name = filename.split('/')[0]

        if bucket_name in BACKENDS[namespace][S3Loader.parameter_name]:
            # get the specified bucket
            bucket = s3.Bucket(BACKENDS[namespace][S3Loader.parameter_name][bucket_name])
        else:
            raise NotFoundError("Namespace {} is not configured.".format(namespace))

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
