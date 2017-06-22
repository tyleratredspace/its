"""
Script to apply transformations to validated images.
"""


# from transformations import BaseTransformation


def process_transforms(img, *transformations):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    # check if a similar transform on the same image is already in cache
    # If len(transformations) == 0 , return image as is

    # apply necessary/easily applicable transforms 
    # according to preset precedence
    # if "resize" in transforms_dict.keys()

    # recursively apply transformations all other transformations
    # result_img = ITSTransformer.apply_transformations(transforms_dict)


def apply_multiple_transforms(img, transformations_dict):

    """
    Recursively applies image transformations.
    """
