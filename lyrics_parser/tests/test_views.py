import unittest
import json

from flask import url_for

from lyrics_parser import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.test_request_context()
        self.app_context.push()

    def test_index(self):
        response = self.app.get(url_for("index"))

        assert response.status_code == 200
        assert b"Search for an artist" in response.data

    def test_search(self):
        response = self.app.get(url_for("search", q="test"))

        assert response.status_code == 200

    def test_results(self):
        response = self.app.get(
            url_for("results", artist_id=9605, artist_name="Om (band)")
        )

        assert response.status_code == 200
        assert b"Om (band)" in response.data

    def test_parse(self):
        response = self.app.get(
            url_for(
                "parse",
                total_count=1,
                completed=0,
                url="https://genius.com/Om-band-gebel-barkal-lyrics",
                songs='{}'
            )
        )

        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert "html" in json_data.keys()
        assert "songs" in json_data.keys()


if __name__ == "__main__":
    unittest.main()
