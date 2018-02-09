from collections import Counter
import string

from bs4 import BeautifulSoup
import requests


MOST_COMMON_WORDS = [
    "a",
    "about",
    "all",
    "also",
    "and",
    "as",
    "at",
    "be",
    "because",
    "but",
    "by",
    "can",
    "come",
    "could",
    "day",
    "do",
    "even",
    "find",
    "first",
    "for",
    "from",
    "get",
    "give",
    "go",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "I",
    "if",
    "in",
    "into",
    "it",
    "its",
    "just",
    "know",
    "like",
    "look",
    "make",
    "man",
    "many",
    "me",
    "more",
    "my",
    "new",
    "no",
    "not",
    "now",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "our",
    "out",
    "people",
    "say",
    "see",
    "she",
    "so",
    "some",
    "take",
    "tell",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "thing",
    "think",
    "this",
    "those",
    "time",
    "to",
    "two",
    "up",
    "use",
    "very",
    "want",
    "way",
    "we",
    "well",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "year",
    "you",
    "your"
]


class LyricParser:
    def __init__(self, artist_id):
        self.base_url = "https://api.genius.com"
        self.band_url = "/artists/{}".format(artist_id)
        self.headers = {
            "Authorization": "Bearer {}".format("umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa")
        }
        self.all_lyrics = []
        self.songs = []
        self.translator = str.maketrans('', '', string.punctuation)
        self.data = []

    def _make_request(self, page=1):
        return requests.get(
            "{}{}/songs?page={}".format(self.base_url, self.band_url, page),
            headers=self.headers
        )

    def _add_songs(self, result):
        for song in result:
            if song["primary_artist"]["api_path"] == self.band_url:
                self.songs.append(song["url"])

    def _get_lyrics(self):
        for song in self.songs:
            song_response = requests.get(song,headers=self.headers)
            soup = BeautifulSoup(song_response.text, "html.parser")
            lyrics = soup.find_all("div", {"class": "lyrics"})[0].get_text()
            self.all_lyrics.extend(
                lyrics.translate(self.translator).lower().split()
            )

    def _get_songs(self, page):
        if page is None:
            return

        response = self._make_request(page)
        self._add_songs(response.json()["response"]["songs"])
        return self._get_songs(response.json()["response"]["next_page"])

    def _process_lyrics(self):
        interesting_words = [word for word in self.all_lyrics if word not in MOST_COMMON_WORDS]
        data = Counter(interesting_words)
        for word in data.most_common(10):
            self.data.append({"word": word[0].capitalize(), "count": word[1]})

    def fetch_song_data(self):
        self._get_songs(1)
        return self.songs

    def run(self):
        self._get_songs(1)
        self._get_lyrics()
        self._process_lyrics()
        return self.data
