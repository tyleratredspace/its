from unittest import TestCase

from its.application import app


class TestRedirects(TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_bad_resize_argument(self):
        response = self.client.get("/tests/images/test.png/?resize=bad")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "Missing width or height. Both width and height are required" in body

    def test_bad_format_argument(self):
        response = self.client.get("/tests/images/test.png/?format=bad")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "Format must be jpeg, png or webp" in body

    def test_zero_fit_argument(self):
        response = self.client.get("/tests/images/test.png/?fit=10x0")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "Crop height must be greater than 0" in body

    def test_strange_punctuation_legacy_resize(self):
        response = self.client.get("/tests/images/test.png.resize.78x34..png")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "Format must be jpeg, png or webp" in body

    def test_strange_arguments_legacy_pipeline(self):
        response = self.client.get(
            "/tests/images/test.png.resize.640x360.png.fit.480x270.png"
        )
        assert response.status_code == 400
