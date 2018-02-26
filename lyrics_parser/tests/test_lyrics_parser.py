import unittest

from lyrics_parser.helpers.parser import Parser


class LyricParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser({})

    def test_get_lyrics(self):
        self.parser.add_song("https://genius.com/Om-band-gebel-barkal-lyrics")

        assert "Gebel Barkal" in self.parser.songs.keys()
        assert "sentiment" in self.parser.songs["Gebel Barkal"].keys()
        assert "themes" in self.parser.songs["Gebel Barkal"].keys()
        assert "word frequencies" in self.parser.songs["Gebel Barkal"].keys()

    def test_process_lyrics(self):
        self.parser.add_song("https://genius.com/Om-band-gebel-barkal-lyrics")
        self.parser.add_song("https://genius.com/Om-band-addis-lyrics")
        self.parser.add_song("https://genius.com/Om-band-annapurna-lyrics")

        data = self.parser.process_all_lyrics()
        assert data["word frequencies"][0][0] == "Freedom" and\
               data["word frequencies"][0][1] == 10


if __name__ == "__main__":
    unittest.main()
