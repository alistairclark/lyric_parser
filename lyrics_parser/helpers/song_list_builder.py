import requests


class SongListBuilder:
    """
    Build up a list of URLs corresponding to songs by an artist.
    """
    def __init__(self, artist_id):
        self.base_url = "https://api.genius.com"
        self.band_url = "/artists/{}".format(artist_id)
        self.headers = {
            "Authorization": "Bearer {}".format(
                "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa"
            )
        }
        self.songs = []

    def _make_request(self, page=1):
        return requests.get(
            "{}{}/songs?page={}".format(self.base_url, self.band_url, page),
            headers=self.headers
        )

    def _add_songs(self, result):
        """ Check primary artist before adding the song to the list.

        For some reason the Genius API returns songs that are unrelated to the
        artist you're looking for, so filter them out.
        """
        for song in result:
            if song["primary_artist"]["api_path"] == self.band_url:
                self.songs.append(song["url"])

    def _get_songs(self, page):
        """Get URLs for all songs listed by artist

        Recursively iterate through the pages of songs for an artist and
        add song to list. Stop when the next_page field is null.

        :param page: The current page

        :return: Return nothing when complete. Otherwise recursively call
        this method with the next_page number.
        """
        if page is None:
            return

        response = self._make_request(page)
        self._add_songs(response.json()["response"]["songs"])
        return self._get_songs(response.json()["response"]["next_page"])

    def get_song_data(self):
        self._get_songs(1)
        return self.songs
