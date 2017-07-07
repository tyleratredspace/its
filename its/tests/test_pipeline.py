from unittest import TestCase
from PIL import Image, ImageChops
from pathlib import Path
import itertools
from math import sqrt
from pipeline.pipeline import process_transforms

def get_pixels(image):
    # List of all the possible coordinates in the image
    coords = list(itertools.product(range(image.width), range(image.height)))
    # list of all pixels in the image
    pixels = [ image.getpixel(coord) for coord in coords ]

    return pixels

def compare_pixels(img1, img2):

    img1_pixels = get_pixels(img1)
    img2_pixels = get_pixels(img2)
    matches = 0
    total = len(img1_pixels) # both images should have the same number of pixels

    for pixel_pair in zip(img1_pixels, img2_pixels):
        if pixel_pair[0] == pixel_pair[1]:
            matches += 1

    return matches / total

def eu_norm(image):
    """
    Calculates the euclidean norm of the pixels of a grayscale image
    """
    pixels = get_pixels(image)
    norm = sum([ pow(sqrt(pix), 2 ) for pix in pixels ])

    return norm

class TestCropTransform(TestCase):

    @classmethod
    def setUpClass(self):
        # current directory / images
        self.img_dir = Path(__file__).parents[0] / "images"

    def test_default_crop_no_alpha(self):
        test_image = Image.open(self.img_dir / "middle.png")
        test_image.info['filename'] = "middle.png"
        query = {'crop':'1x1'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = eu_norm(diff_gray) # calculate the norm
        self.assertNotAlmostEqual(0, norm) # the difference would be 0 if they were the same

    def test_focal_crop_no_alpha(self):
        test_image = Image.open(self.img_dir / "top_left.png")
        test_image.info['filename'] = "top_left.png"
        query = {'crop':'1x1x0x0'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = eu_norm(diff_gray) # calculate the norm
        self.assertAlmostEqual(0, norm)

    def test_smart_crop_no_alpha(self):
        test_image = Image.open(self.img_dir / "bottom_right_focus-99x99.png")
        test_image.info['filename'] = "bottom_right_focus-99x99.png"
        query = {'crop':'1x1'}
        expected = Image.open(self.img_dir / "expected/blue_pixel.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = eu_norm(diff_gray) # calculate the norm
        self.assertAlmostEqual(0, norm)

class TestOverlayTransform(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.img_dir = Path(__file__).parents[0] / "images"
        self.overlays = {'five':'images/five.png'}

    def test_overlay(self):
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'overlay':'45x45xits/tests/images/five.png'}
        expected = Image.open(self.img_dir / "expected/abstract_overlay_five.png")
        actual = process_transforms(test_image, query)
        diff = ImageChops.difference(expected, actual)
        diff_gray = diff.convert('L') # convert to grayscale, 'LA' for L with alpha channel
        norm = eu_norm(diff_gray) # calculate the norm
        self.assertAlmostEqual(0, norm)

class TestResizeTransform(TestCase):

    @classmethod
    def setUpClass(self):
        # current directory / images
        self.img_dir = Path(__file__).parents[0] / "images"
        self.threshold = 0.5

    def test_resize_size(self):
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'resize':'10x10'}
        result = process_transforms(test_image, query)
        self.assertEqual(result.size, (10, 10))

    def test_resize_integrity(self):
        test_image = Image.open(self.img_dir / "test.png")
        test_image.info['filename'] = "test.png"
        query = {'resize':'100x100'}
        expected = Image.open(self.img_dir / "expected/test_resize.png")
        actual = process_transforms(test_image, query)
        comparison = compare_pixels(expected, actual)
        self.assertGreaterEqual(comparison, self.threshold)

if __name__ == '__main__':
    unittest.main()