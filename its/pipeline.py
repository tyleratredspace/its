"""
Script to apply transformations to validated images.
"""

from transformations import BaseTransform, ResizeTransform
from errors import ITSTransformError

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
        img = ResizeTransform.apply_transform(img, transforms['resize'])

    for tclass in transform_classes:
        if tclass.slug in transforms.keys() and tclass.slug not in first_applied:
            # split the query string for the class
            transforms[tclass.slug] = transforms[tclass.slug].split('x')
            img = tclass.apply_transform(img, transforms[tclass.slug])

    img.info = img_info # some transformations might overwrite the info dict
    # image conversion and compression
    # cache result
    return img
