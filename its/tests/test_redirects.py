from unittest import TestCase

from its.application import APP


class TestRedirects(TestCase):
    @classmethod
    def setUpClass(self):
        APP.config["TESTING"] = True
        self.client = APP.test_client()

    def test_redirect(self):
        response = self.client.get(
            "/station-images/StationColorProfiles/color/WGBH.png.resize.240x120.png"
        )
        assert response.status_code == 301
        assert (
            response.location
            == "https://station-service.example.com/station/image-redirects/?url=http://localhost/station-images/StationColorProfiles/color/WGBH.png.resize.240x120.png"
        )
