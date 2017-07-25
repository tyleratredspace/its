"""
Script to apply transformations to validated images.
"""
import re
from .transformations import BaseTransform


def process_transforms(img, query, *args):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    transform_classes = BaseTransform.__subclasses__()
    img_info = img.info
    transform_order = {"resize": None, "crop": None, "overlay": None}

    # check if a similar transform on the same image is already in cache

    if len(query) == 0:  # no transforms; return image as is
        return img

    # assign each subclass to it's slug in the order dict
    for tclass in transform_classes:
        transform_order[tclass.slug] = tclass

    # loop through the order dict and apply the transforms
    for transform in transform_order:
        if transform in query:
            query[transform] = query[transform].split('x')
            img = transform_order[transform].apply_transform(img, query[transform])

    if img.format is None and 'filename' in img_info.keys():
        # attempt to grab the filetype from the filename
        file_type = re.sub('.+?(\.)', '', img_info['filename'], flags=re.IGNORECASE)
        if file_type.lower() == "jpg" or file_type.lower() == "jpeg":
            img.format = "JPEG"
        else:
            img.format = file_type.upper()

    return img
