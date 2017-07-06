from unittest import TestCase
from PIL import Image, ImageChops, ImageMath
from pathlib import Path
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

    # @classmethod
    # def eu_norm(self, image):
        """
        Calculates the euclidean norm of the pixels of an image
        """
        # coords = list()

        # for x in range(1, image.width):
        #     for y in range(1, image.height):
        #         coords.append((x,y))
        # pixels = [ image.getpixel(coord) for coord in coords ]

        # norm = [ pow( pow(pix, 0.5), 2 ) for pix in pixels ]

        # norm = sum(norm)

        # return norm

    def test_default_crop(self):
        test_image = Image.open(self.img_dir / "top_left.png")
        test_image.info['filename'] = "top_left.png"
        query = {'crop':'1x1'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query) 
        diff = ImageChops.difference(expected, actual)
        # norm = self.eu_norm(diff) # calculate the norm
        norm = 0
        self.assertEqual(0, norm)

    # def test_focal_crop(self):

    #   self.Assert

    # def test_smart_crop(self):

    #   self.Assert

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