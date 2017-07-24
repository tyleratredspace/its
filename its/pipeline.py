"""
Script to apply transformations to validated images.
"""
import re
from .transformations import BaseTransform, ResizeTransform
# from .errors import ITSTransformError
from .optimize import optimize


def process_transforms(img, transforms, *args):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    transform_classes = BaseTransform.__subclasses__()
    img_info = img.info
    first_applied = ['resize']

    # check if a similar transform on the same image is already in cache

    if len(transforms) == 0:  # no transforms; return image as is
        return img

    # apply necessary/easily applicable transforms
    # according to preset precedence
    if "resize" in transforms.keys():
        transforms['resize'] = transforms['resize'].split('x')
        img = ResizeTransform.apply_transform(img, transforms['resize'])

    for tclass in transform_classes:
        if tclass.slug in transforms.keys() and tclass.slug not in first_applied:
            # split the query string for the class
            transforms[tclass.slug] = transforms[tclass.slug].split('x')
            img = tclass.apply_transform(img, transforms[tclass.slug])

    if img.format is None and 'filename' in img_info.keys():
        # attempt to grab the filetype from the filename
        file_type = re.sub('(\.).+', '', img_info['filename'], flags=re.IGNORECASE)
        if file_type.lower() == "jpg" or file_type.lower() == "jpeg":
            img.format = "JPEG"
        else:
            img.format = file_type.upper()
    # print(img.info)
    # img.info = img_info  # some transformations might overwrite the info dict
    # print(img_info)
    # image conversion and compression
    # cache result
    img = optimize(img, transforms)
    return img
