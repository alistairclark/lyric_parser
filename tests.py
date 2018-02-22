import unittest
import json

from flask import url_for

from views import app
from parser import Parser
from song_list_builder import SongListBuilder


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
                all_lyrics='["this is a test"]'
            )
        )

        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert "all_lyrics" in json_data.keys()
        assert "html" in json_data.keys()
        assert "songs" in json_data.keys()


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

        assert "Gebel Barkal" in self.parser.songs.keys()
        assert "sentiment" in self.parser.songs["Gebel Barkal"].keys()
        assert "themes" in self.parser.songs["Gebel Barkal"].keys()
        assert "word frequencies" in self.parser.songs["Gebel Barkal"].keys()

    def test_process_lyrics(self):
        self.parser.get_lyrics(
            "https://genius.com/Om-band-gebel-barkal-lyrics"
        )
        self.parser.get_lyrics(
            "https://genius.com/Om-band-gebel-barkal-lyrics"
        )
        self.parser.get_lyrics(
            "https://genius.com/Om-band-gebel-barkal-lyrics"
        )

        data = self.parser.process_all_lyrics()

        assert data[0][0] == "Series" and data[0][1] == 3


if __name__ == "__main__":
    unittest.main()
