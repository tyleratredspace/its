import logging
import re
from typing import Sequence, Union

from PIL import Image, ImageOps
from PIL.ImageFilter import GaussianBlur

from ..errors import ITSClientError, ITSTransformError
from ..settings import DELIMITERS_RE, FOCUS_KEYWORD
from .base import BaseTransform

LOGGER = logging.getLogger(__name__)


class BlurTransform(BaseTransform):

    slug = "blur"

    @staticmethod
    def derive_parameters(query: str) -> Sequence[str]:
        return re.split(DELIMITERS_RE, query)

    @staticmethod
    def apply_transform(
        img: Image.Image, parameters: Sequence[Union[str, int]]
    ) -> Image.Image:
        """
        Blurs an image
        """
        blurred_image = img.filter(GaussianBlur(radius=2))
        return blurred_image
