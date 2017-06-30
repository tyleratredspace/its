"""
Script to apply transformations to validated images.
"""

from transformations import BaseTransform, ResizeTransform


def process_transforms(img, *transforms):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    new_img = None
    transform_classes = BaseTransform.__subclasses__()
    first_applied = ['resize']
    transforms = transforms[0]
    # check if a similar transform on the same image is already in cache

    if len(transforms) == 0:  # no transforms; return image as is
        new_img = img
        return new_img

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
