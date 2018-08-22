from unittest import TestCase

from its.application import app


class TestClientErrorHandling(TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_invalid_namespace(self):
        response = self.client.get("/invalid-namespace/image.jpg")
        body = response.data.decode("utf-8")
        assert response.status_code == 400
        assert "invalid-namespace is not a configured namespace" in body
