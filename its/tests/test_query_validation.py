from unittest import TestCase

from its.application import app


class TestRedirects(TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_bad_resize_argument(self):
        response = self.client.get("/tests/images/test.png/?resize=bad")
        assert response.status_code == 400

    def test_bad_format_argument(self):
        response = self.client.get("/tests/images/test.png/?format=bad")
        assert response.status_code == 400

    def test_zero_fit_argument(self):
        response = self.client.get("/tests/images/test.png/?fit=10x0")
        assert response.status_code == 400

    def test_strange_punctuation_legacy_resize(self):
        response = self.client.get("/tests/images/test.png.resize.78x34..png")
        assert response.status_code == 400

    def test_strange_arguments_legacy_pipeline(self):
        response = self.client.get(
            "/tests/images/test.png.resize.640x360.png.fit.480x270.png"
        )
        assert response.status_code == 400
