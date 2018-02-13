import unittest

from flask import url_for

from lyrics_parser.parser import Parser
from lyrics_parser.song_list_builder import SongListBuilder
from lyrics_parser.views import app


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
        response = self.app.get(url_for("results", q=9605))
        assert response.status_code == 200

    def test_parse(self):
        response = self.app.get(
            url_for(
                "parse",
                total_count=1,
                completed=0,
                url="https://genius.com/Om-band-gebel-barkal-lyrics",
                all_lyrics='["this is a test"]'
            )
        )

        assert response.status_code == 200


class SongListBuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.song_list_builder = SongListBuilder(9605)

    def test_fet_song_data(self):
        songs = self.song_list_builder.fetch_song_data()
        assert len(songs) > 0


class LyricParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser([])

    def test_get_lyrics(self):
        self.parser.get_lyrics(
            "https://genius.com/Om-band-gebel-barkal-lyrics"
        )
        assert self.parser.all_lyrics != ""

    def test_process_lyrics(self):
        self.parser.all_lyrics = [
            "test", "test", "interesting", "words"
        ]
        data = self.parser.process_lyrics()
        assert data[0]["word"] == "Test" and data[0]["count"] == 2


if __name__ == "__main__":
    unittest.main()
