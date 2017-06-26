"""
Script to apply transformations to validated images.
"""

from transformations import BaseTransform, ResizeTransform


def process_transforms(img, transforms, *args):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    transform_classes = BaseTransform.__subclasses__()
    first_applied = ['resize']
    img_info = args

    # check if a similar transform on the same image is already in cache

    if len(transforms) == 0:  # no transforms; return image as is
        return img

    # apply necessary/easily applicable transforms
    # according to preset precedence
    if "resize" in transforms.keys():
        img = ResizeTransform.apply_transform(img, transforms['resize'])

    for tclass in transform_classes:
        if tclass.slug in transforms.keys() and tclass.slug not in first_applied:
            img = tclass.apply_transform(img, transforms[tclass.slug])

    # cache resulting image
    # return the image in browser
    return "completed"
