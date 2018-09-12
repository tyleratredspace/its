from unittest import TestCase

from its.application import APP

from . import test_vcr


class TestRedirects(TestCase):
    @classmethod
    def setUpClass(self):
        APP.config["TESTING"] = True
        self.client = APP.test_client()

    @test_vcr.use_cassette()
    def test_merlin_http(self):
        response = self.client.get(
            "/merlin/s3.amazonaws.com/pbs.merlin.cdn.prod/program_pages/IndependentLens_480x270.380x212.png.fit.640x360.png"
        )
        assert response.status_code == 200

    @test_vcr.use_cassette()
    def test_self_referential_http_backend_use(self):
        response = self.client.get("/merlin/localhost/tests/images/test.png")
        assert response.status_code == 200

    @test_vcr.use_cassette()
    def test_http_backend_404(self):
        response = self.client.get(
            "/merlin/s3.amazonaws.com/pbs.merlin.cdn.prod/some-fake-thing.jpg.fit.646x246.jpg"
        )
        assert response.status_code == 404
