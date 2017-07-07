from unittest import TestCase
from PIL import Image, ImageChops
from pathlib import Path
import itertools
from math import sqrt
from pipeline.pipeline import process_transforms


class TestCropTransform(TestCase):
    """
    """

    @classmethod
    def setUpClass(self):
        # current directory / images
        self.img_dir = Path(__file__).parents[0] / "images"
        # self.threshold = 0.5

    # @classmethod
    # def tearDownClass(self):

    @classmethod
    def eu_norm(self, image):
        """
        Calculates the euclidean norm of the pixels of a grayscale image
        """
        # List of all the possible coordinates in the image
        coords = list(itertools.product(range(image.width), range(image.height)))
        # list of all pixels in the image
        pixels = [ image.getpixel(coord) for coord in coords ]
        norm = sum([ pow(sqrt(pix), 2 ) for pix in pixels ])

        return norm

    def test_default_crop_no_alpha(self):
        test_image = Image.open(self.img_dir / "middle.png")
        test_image.info['filename'] = "middle.png"
        query = {'crop':'1x1'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = self.eu_norm(diff_gray) # calculate the norm
        self.assertNotAlmostEqual(0, norm) # the difference would be 0 if they were the same

    def test_focal_crop(self):
        test_image = Image.open(self.img_dir / "top_left.png")
        test_image.info['filename'] = "top_left.png"
        query = {'crop':'1x1x0x0'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = self.eu_norm(diff_gray) # calculate the norm
        self.assertAlmostEqual(0, norm)

    def test_smart_crop(self):
        test_image = Image.open(self.img_dir / "bottom_right_focus-99x99.png")
        test_image.info['filename'] = "bottom_right_focus-99x99.png"
        query = {'crop':'1x1'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = self.eu_norm(diff_gray) # calculate the norm
        self.assertAlmostEqual(0, norm)

# class TestOverlayTransform(TestCase):
#   """
#   """

#   @classmethod
#   def setUpClass(self):

#   @classmethod
#   def tearDownClass(self):

# class TestResizeTransform(TestCase):
#   """
#   """

#   @classmethod
#   def setUpClass(self):

#   @classmethod
#   def tearDownClass(self):

if __name__ == '__main__':
    unittest.main()