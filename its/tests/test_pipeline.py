import unittest
from unittest import TestCase
from unittest.mock import patch
from pathlib import Path
from PIL import Image
import itertools
from io import BytesIO
import os
import tempfile
from its.pipeline import process_transforms
from its.optimize import optimize


def get_pixels(image):
    # List of all the possible coordinates in the image
    coords = list(itertools.product(range(image.width), range(image.height)))
    # list of all pixels in the image
    pixels = [image.getpixel(coord) for coord in coords]

    return pixels


def compare_pixels(img1, img2):
    img1_pixels = get_pixels(img1)
    img2_pixels = get_pixels(img2)
    matches = 0
    total = len(img1_pixels)  # both images should have the same number of pixels

    for pixel_pair in zip(img1_pixels, img2_pixels):
        if pixel_pair[0] == pixel_pair[1]:
            matches += 1
        else:
            r1, g1, *b1 = pixel_pair[0]
            r2, g2, *b2 = pixel_pair[1]
            test = "%d %d %d vs %d %d %d" % (r1, g1, b1[0], r2, g2, b2[0])
            print(test)
            diff = "%d %d %d" % (abs(r1 - r2), abs(g1 - g2), abs(b1[0] - b2[0]))
            print(diff)

    return matches / total


class TestFitTransform(TestCase):

    @classmethod
    def setUpClass(self):
        self.img_dir = Path(__file__).parent / "images"

    @patch('its.transformations.fit.FitTransform.apply_transform')
    def test_default_fit_no_alpha(self, MockFitTransform):
        fit_transform = MockFitTransform()
        test_image = Image.open(self.img_dir / "middle.png")
        test_image.info['filename'] = "middle.png"
        query = {'fit': '100x100'}
        fit_transform.return_value = True
        fit_transform(test_image, query)
        fit_transform.assert_called_with(test_image, query)

    @patch('its.transformations.fit.FitTransform.apply_transform')
    def test_focal_fit_no_alpha(self, MockFitTransform):
        fit_transform = MockFitTransform()
        test_image = Image.open(self.img_dir / "top_left.png")
        test_image.info['filename'] = "top_left.png"
        query = {'fit': '1x1x1x1'}
        fit_transform.return_value = True
        fit_transform(test_image, query)
        fit_transform.assert_called_with(test_image, query)

    @patch('its.transformations.fit.FitTransform.apply_transform')
    def test_focal_1x1_no_alpha(self, MockFitTransform):
        fit_transform = MockFitTransform()
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'fit': '28x34x1x1'}
        fit_transform.return_value = True
        fit_transform(test_image, query)
        fit_transform.assert_called_with(test_image, query)

    @patch('its.transformations.fit.FitTransform.apply_transform')
    def test_focal_100x100_no_alpha(self, MockFitTransform):
        fit_transform = MockFitTransform()
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'fit': '1x1x100x100'}
        fit_transform.return_value = True
        fit_transform(test_image, query)
        fit_transform.assert_called_with(test_image, query)

    @patch('its.transformations.fit.FitTransform.apply_transform')
    def test_smart_70x1_no_alpha(self, MockFitTransform):
        fit_transform = MockFitTransform()
        test_image = Image.open(self.img_dir / "abstract_focus-70x1.png")
        test_image.info['filename'] = "abstract_focus-70x1.png"
        query = {'fit': '5x100'}
        fit_transform.return_value = True
        fit_transform(test_image, query)
        fit_transform.assert_called_with(test_image, query)


class TestOverlayTransform(TestCase):

    @classmethod
    def setUpClass(self):
        self.img_dir = Path(__file__).parent / "images"
        self.overlays = {'five': 'images/five.png'}
        self.threshold = 0.85

    def test_overlay(self):
        print(self.img_dir)

        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'overlay': '45x45x' + self.overlays['five']}
        expected = Image.open(self.img_dir / "expected/abstract_overlay_five.png")
        actual = process_transforms(test_image, query)
        compare_pixels(expected, actual)

    def test_overlay_12x78(self):
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'overlay': '12x78x' + self.overlays['five']}
        expected = Image.open(self.img_dir / "expected/abstract_five_12x78.png")
        actual = process_transforms(test_image, query)
        comparison = compare_pixels(expected, actual)
        self.assertGreaterEqual(comparison, self.threshold)


class TestResizeTransform(TestCase):

    @classmethod
    def setUpClass(self):
        # current directory / images
        self.img_dir = Path(__file__).parent / "images"
        self.threshold = 0.5

    def test_resize_size(self):
        test_image = Image.open(self.img_dir / "abstract.png")
        test_image.info['filename'] = "abstract.png"
        query = {'resize': '10x10'}
        result = process_transforms(test_image, query)
        self.assertEqual(result.size, (10, 10))

    def test_resize_integrity_smaller(self):
        test_image = Image.open(self.img_dir / "test.png")
        test_image.info['filename'] = "test.png"
        query = {'resize': '100x100'}
        expected = Image.open(self.img_dir / "expected/test_resize.png")
        actual = process_transforms(test_image, query)
        # can't use norm since resizing can cause noise
        comparison = compare_pixels(expected, actual)
        self.assertGreaterEqual(comparison, self.threshold)

    def test_resize_integrity_larger(self):
        test_image = Image.open(self.img_dir / "test.png")
        test_image.info['filename'] = "test.png"
        query = {'resize': '700x550'}
        expected = Image.open(self.img_dir / "expected/test_resize_700x550.png")
        actual = process_transforms(test_image, query)
        comparison = compare_pixels(expected, actual)
        self.assertGreaterEqual(comparison, self.threshold)


class TestImageResults(TestCase):

    @classmethod
    def setUpClass(self):
        # current directory / images
        self.img_dir = Path(__file__).parent / "images"

    def test_jpg_progressive(self):
        test_image = Image.open(self.img_dir / "middle.png")
        result = optimize(test_image, {'format': 'jpg'})
        self.assertEqual(result.info['progressive'], 1)

    def test_jpg_quality_vs_size(self):
        test_image = Image.open(self.img_dir / "middle.png")
        quality_1 = optimize(test_image, {'quality': 1, 'format': 'jpg'})
        with tempfile.NamedTemporaryFile(dir=".", delete=True) as tmp_file_1:
            quality_1.save(tmp_file_1.name, format=quality_1.format)
            q1_size = os.stat(tmp_file_1.name).st_size

        quality_10 = optimize(test_image, {'quality': 10, 'format': 'jpg'})
        with tempfile.NamedTemporaryFile(dir=".", delete=True) as tmp_file_2:
            quality_10.save(tmp_file_2.name, format=quality_10.format)
            q10_size = os.stat(tmp_file_2.name).st_size

        self.assertLessEqual(q1_size, q10_size)

    def test_png_quality_vs_size(self):
        test_image = Image.open(self.img_dir / "test.png")
        quality_1 = optimize(test_image, {'quality': '1'})
        with tempfile.NamedTemporaryFile(dir=".", delete=True) as tmp_file_1:
            quality_1.save(tmp_file_1.name, format=quality_1.format)
            q1_size = os.stat(tmp_file_1.name).st_size

        quality_10 = optimize(test_image, {'quality': '10'})
        with tempfile.NamedTemporaryFile(dir=".", delete=True) as tmp_file_2:
            quality_10.save(tmp_file_2.name, format=quality_10.format)
            q10_size = os.stat(tmp_file_2.name).st_size

        self.assertLessEqual(q1_size, q10_size)

    def test_svg_passthrough(self):
        test_image = BytesIO(open(self.img_dir / "wikipedia_logo.svg", "rb").read())
        query = {
            'fit': '10x10', 'format': 'png',
            'resize': '500x500', 'filename': "wikipedia_logo.svg"
        }
        result = process_transforms(test_image, query)
        result = optimize(result, query)
        self.assertEqual(isinstance(result, BytesIO), True)


if __name__ == '__main__':
    unittest.main()
