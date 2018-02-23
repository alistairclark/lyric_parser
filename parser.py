from collections import Counter
from functools import reduce
import re
from statistics import mean

from bs4 import BeautifulSoup
from nltk.corpus import wordnet
import requests
from textblob import TextBlob
from textblob import Word

from helpers import STOP_WORDS


class Parser:
    def __init__(self, songs):
        # Set authorization header in order to use Genius API
        # (https://docs.genius.com/)
        self.headers = {
            "Authorization": "Bearer {}".format(
                "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa"
            )
        }

        self.songs = songs

    def _get_lyrics_and_title(self, response):
        """
        Parse the content of an HTTP response (using BeautifulSoup) and get
        the lyrics and title for the song.
        """
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find_all(
            "h1", {"class": "header_with_cover_art-primary_info-title"}
        )[0].get_text()

        lyrics = soup.find_all("div", {"class": "lyrics"})[0].get_text()

        return title, lyrics

    def _format_word(self, word):
        """
        Lemmatize (https://en.wikipedia.org/wiki/Lemma_(morphology)),
        capitalize, and remove punctuation (other than apostrophes).
        """
        punctuation_stripped = re.sub(r"[^\w\d'\s]+", '', word)
        lemmatized = Word(punctuation_stripped).lemmatize()
        capitalized = lemmatized.capitalize()

        return capitalized

    def _remove_common_words(self, lyrics):
        return [word for word in lyrics.split() if word.lower() not in STOP_WORDS]

    def _prepare_lyrics(self, lyrics):
        """
        Remove common English words from lyrics, remove blank items, and format
        the remaining words.
        """
        uncommon_words = self._remove_common_words(lyrics)
        processed_string = list(map(
            self._format_word,
            uncommon_words
        ))

        strip_blanks = list(
            filter(lambda x : x.strip() != "", processed_string)
        )

        return strip_blanks


    def _analyse_sentiment(self, lyrics):
        """
        Break the lyrics down into TextBlob Sentence objects. Create a list
        of the Sentiments for those Sentences. Return the mean polarity and
        subjectivity of the song.
        """
        sentences = TextBlob(lyrics).sentences
        sentiments = [sentence.sentiment for sentence in sentences]

        mean_polarity = mean(
            [sentiment.polarity for sentiment in sentiments]
        )

        mean_subjectivity = mean(
            [sentiment.subjectivity for sentiment in sentiments]
        )

        return mean_polarity, mean_subjectivity

    def _analyse_themes(self, lyrics):
        """
        Create a list of Synsets (http://www.nltk.org/howto/wordnet.html),
        find the most common hypernyms (https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy),
        and count them and return the 5 most common.
        """
        synsets = []
        for word in lyrics:
            synsets.extend(wordnet.synsets(word))

        hypernyms = []
        for synset in synsets:
            hypernyms.extend(synset.hypernyms())

        # Return the name of the first lemma of each hypernym (so we can
        # deal with English words)
        hypernym_lemmas = [
            x.lemma_names()[0].replace("_", " ").capitalize() for x in hypernyms
        ]

        counter = Counter(hypernym_lemmas)
        return counter.most_common(3)

    def _get_word_frequencies(self, words):
        return Counter(words)

    def _get_mean_polarity(self):
        polarities = []
        for key, value in self.songs.items():
            if value["sentiment"][0] != '':
                polarities.append(float(value["sentiment"][0]))

        if len(polarities) > 0:
            return mean(polarities)
        else:
            return None

    def _get_mean_subjectivity(self):
        subjectivities = []
        for key, value in self.songs.items():
            if value["sentiment"][1] != '':
                subjectivities.append(float(value["sentiment"][1]))

        if len(subjectivities) > 0:
            return mean(subjectivities)
        else:
            return None

    def get_lyrics(self, url):
        response = requests.get(url, headers=self.headers)
        title, lyrics = self._get_lyrics_and_title(response)
        words = self._prepare_lyrics(lyrics)

        self.songs[title] = {
            "word frequencies": self._get_word_frequencies(words),
            "lyrics": lyrics,
            "sentiment": self._analyse_sentiment(lyrics),
            "themes": self._analyse_themes(words)
        }

    def process_all_lyrics(self):
        counter = Counter([])
        for key, value in self.songs.items():
            counter += value["word frequencies"]

        polarity = self._get_mean_polarity()
        subjectivity = self._get_mean_subjectivity()

        themes = []
        for key, value in self.songs.items():
            string_only = [theme[0] for theme in value["themes"]]
            themes.extend(string_only)

        print(themes)

        data = {
            "word frequencies": counter.most_common(10),
            "polarity": polarity,
            "subjectivity": subjectivity,
            "theme frequencies": Counter(themes).most_common(5)
        }

        return data
