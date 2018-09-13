from unittest import TestCase

from its.application import APP


class TestClientErrorHandling(TestCase):
    @classmethod
    def setUpClass(self):
        APP.config["TESTING"] = True
        self.client = APP.test_client()

    def test_invalid_namespace(self):
        response = self.client.get("/invalid-namespace/image.jpg")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "invalid-namespace is not a configured namespace" in body

    def test_non_image_file(self):
        response = self.client.get("/tests/images/not-an-image.jpg")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert " tests/images/not-an-image.jpg is not an image file" in body
