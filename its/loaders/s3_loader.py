from .base import BaseLoader
from ..errors import NotFoundError
from PIL import Image
import boto3
from botocore.exceptions import ClientError
from io import BytesIO


class S3Loader(BaseLoader):

    slug = "s3"

    def get_fileobj(namespace, filename):
        """
        Given a namespace (or directory name) and a filename, returns a file-like or bytes-like object.
        """
        # get the s3 resource
        s3 = boto3.resource('s3')

        # get the specified bucket
        bucket = s3.Bucket(namespace)

        bucket.wait_until_exists()
        # create an empty bytes object to store the image bytes in
        file_obj = BytesIO()
        bucket.download_fileobj(filename, file_obj)

        return file_obj

    def load_image(namespace, filename):
        """
        Loads image from file system
        """
        try:

            file_obj = get_fileobj(namespace, filename)
            image = Image.open(file_obj)

        except (ClientError, WaiterError) as e:
            raise NotFoundError(error=str(e))

        return image

