"""
Script to apply transformations to validated images.
"""

from transformations import BaseTransform, ResizeTransform


# from transformations import BaseTransformation


def process_transforms(img, *transformations):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    new_image = None
    transform_classes = BaseTransform.__subclasses__()

    # check if a similar transform on the same image is already in cache

    if len(transformations[0]) == 0:  # no transforms; return image as is
        new_image = img
        return new_image

    # apply necessary/easily applicable transforms 
    # according to preset precedence
    # if "resize" in transforms_dict.keys()
    new_image = ResizeTransform.apply_transformation(img,transformations[0]['resize'])

    # recursively apply transformations all other transformations
    # result_img = ITSTransformer.apply_transformations(transforms_dict)
        

    return new_image


def apply_multiple_transforms(img, transformations_dict):

    """
    Recursively applies image transformations.
    """
