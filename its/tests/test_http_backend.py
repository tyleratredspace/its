from unittest import TestCase

from its.application import app

from . import test_vcr


class TestRedirects(TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @test_vcr.use_cassette()
    def test_merlin_http(self):
        response = self.client.get(
            "/merlin/s3.amazonaws.com/pbs.merlin.cdn.prod/program_pages/IndependentLens_480x270.380x212.png.fit.640x360.png"
        )
        assert response.status_code == 200
