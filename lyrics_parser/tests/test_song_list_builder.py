import unittest

from lyrics_parser.helpers.song_list_builder import SongListBuilder


class SongListBuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.song_list_builder = SongListBuilder(9605)

    def test_get_song_data(self):
        songs = self.song_list_builder.get_song_data()

        assert len(songs) > 0


if __name__ == "__main__":
    unittest.main()
