from typing import Sequence, Union

from PIL import Image


class BaseTransform(object):

    """
    Generic image transform type class
    """

    slug: Union[None, str] = None  # unique string that identifies a given transform

    def __init__(self, arg):
        super(BaseTransform, self).__init__()
        self.arg = arg

    @staticmethod
    def apply_transform(
        img: Image.Image, parameters: Sequence[Union[str, int]]
    ) -> Image.Image:
        raise NotImplementedError
