import requests


class SongListBuilder:
    def __init__(self, artist_id):
        self.base_url = "https://api.genius.com"
        self.band_url = "/artists/{}".format(artist_id)
        self.headers = {
            "Authorization": "Bearer {}".format("umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa")
        }
        self.songs = []

    def _make_request(self, page=1):
        return requests.get(
            "{}{}/songs?page={}".format(self.base_url, self.band_url, page),
            headers=self.headers
        )

    def _add_songs(self, result):
        for song in result:
            if song["primary_artist"]["api_path"] == self.band_url:
                self.songs.append(song["url"])


    def _get_songs(self, page):
        if page is None:
            return

        response = self._make_request(page)
        self._add_songs(response.json()["response"]["songs"])
        return self._get_songs(response.json()["response"]["next_page"])

    def fetch_song_data(self):
        self._get_songs(1)
        return self.songs
