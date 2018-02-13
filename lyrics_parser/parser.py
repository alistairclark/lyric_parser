from collections import Counter
import re
import string

from bs4 import BeautifulSoup
import requests
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
    def __init__(self, lyrics=[]):
        self.headers = {
            "Authorization": "Bearer {}".format("umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa")
        }
        self.all_lyrics = lyrics if lyrics != "" else []
        self.data = []

    def get_lyrics(self, url):
        song_response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(song_response.text, "html.parser")
        lyrics = soup.find_all("div", {"class": "lyrics"})[0].get_text()
        punctuation_stripped= re.sub(r"[^\w\d'\s]+", '', lyrics)
        lemmatized = [Word(word.lower().strip()).lemmatize() for word in punctuation_stripped.split()]
        self.all_lyrics.extend(lemmatized)

    def process_lyrics(self):
        interesting_words = [word for word in self.all_lyrics if word not in MOST_COMMON_WORDS]
        exclude_punctuation = [word for word in interesting_words if word not in string.punctuation]

        data = Counter(exclude_punctuation)
        for word in data.most_common(10):
            self.data.append({"word": word[0].capitalize(), "count": word[1]})

        return self.data
