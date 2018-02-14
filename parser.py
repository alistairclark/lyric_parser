import re
from collections import Counter

import requests
from bs4 import BeautifulSoup
from textblob import Word


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
        "your",
        "[verse]"
    ]


class Parser:
    def __init__(self, lyrics):
        self.headers = {
            "Authorization": "Bearer {}".format(
                "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa"
            )
        }
        self.all_lyrics = lyrics if lyrics != "" else []
        self.data = []

    def _make_soup(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("div", {"class": "lyrics"})[0].get_text()

    def _prepare_string(self, lyrics):
        no_punctuation = re.sub(r"[^\w\d'\s]+", '', lyrics)
        lemmatized = [
            Word(w.lower()).lemmatize().capitalize() for w in no_punctuation.split()
        ]

        return lemmatized

    def _remove_common_words(self):
        self.all_lyrics = [
            word for word in self.all_lyrics
            if word.lower() not in MOST_COMMON_WORDS
        ]

    def get_lyrics(self, url):
        response = requests.get(url, headers=self.headers)
        lyrics = self._make_soup(response)
        prepared_lyrics = self._prepare_string(lyrics)

        self.all_lyrics.extend(prepared_lyrics)

    def process_lyrics(self):
        self._remove_common_words()
        data = Counter(self.all_lyrics)

        return data.most_common(10)
