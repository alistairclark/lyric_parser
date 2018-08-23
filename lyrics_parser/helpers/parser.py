from collections import Counter
import re
from statistics import mean

import nltk
from nltk.corpus import wordnet
from requests_html import HTMLSession
from textblob import TextBlob
from textblob import Word

from lyrics_parser.helpers.helpers import STOP_WORDS


class Parser:
    """
    Build up a dictionary of information about songs by an artist
    and process that information.
    """
    def __init__(self, songs):
        # Set authorization header in order to use Genius API
        # (https://docs.genius.com/)
        self.headers = {
            "Authorization": "Bearer {}".format(
                "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa"
            )
        }

        self.songs = songs

    def _get_lyrics_and_title(self, url):
        session = HTMLSession()
        session.headers = self.headers
        response = session.get(url)

        title = response.html.find(
            ".header_with_cover_art-primary_info-title",
            first=True
        ).text

        lyrics = response.html.find(".lyrics", first=True).text

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
        """
        Exclude common words by comparing lyrics to a list of Stop Words
        (https://en.wikipedia.org/wiki/Stop_words)
        """
        return [word for word in lyrics.split() if word.lower() not in STOP_WORDS]

    def _prepare_lyrics(self, lyrics):
        """
        Remove common English words from lyrics, remove blank items,
        and format the remaining words.
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
        """ Analyse the overall positivty/negativity and
        subjectivity/objectivity of the lyrics in a song.

        Break the lyrics down into TextBlob Sentence objects. Create a list
        of Sentiments for those Sentences. Return the mean polarity and
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
        """ Very roughly establish what concepts are commonly referred to
        by this artist.

        Create a list of Synsets (http://www.nltk.org/howto/wordnet.html),
        find the most common hypernyms (https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy),
        count them and return the 5 most common.
        """
        synsets = []
        for word in lyrics:
            synsets.extend(wordnet.synsets(word))

        hypernyms = []
        for synset in synsets:
            hypernyms.extend(synset.hypernyms())

        # Return the name of the first lemma (https://en.wikipedia.org/wiki/Lemma_(morphology))
        # of each hypernym (so we can deal with English words)
        hypernym_lemmas = [
            x.lemma_names()[0].replace("_", " ").capitalize() for x in hypernyms
        ]

        counter = Counter(hypernym_lemmas)
        return counter.most_common(3)

    def _get_word_frequencies(self, words):
        return Counter(words)

    def _get_mean_polarity(self):
        """
        Calculate the mean polarity (positivity/negativity)
        of all the songs in the dictionary.
        """
        polarities = []
        for key, value in self.songs.items():
            if value["sentiment"][0] != '':
                polarities.append(float(value["sentiment"][0]))

        if len(polarities) > 0:
            return mean(polarities)
        else:
            return None

    def _get_mean_subjectivity(self):
        """
        Calculate the mean subjectivity of all the songs in the dictionary.
        """
        subjectivities = []
        for key, value in self.songs.items():
            if value["sentiment"][1] != '':
                subjectivities.append(float(value["sentiment"][1]))

        if len(subjectivities) > 0:
            return mean(subjectivities)
        else:
            return None

    def add_song(self, url):
        """
        Build a dictionary of information about a song from a given url.

        Add this dictionary to the dictionary of songs.

        :param url: The URL of the song
        """
        title, lyrics = self._get_lyrics_and_title(url)
        words = self._prepare_lyrics(lyrics)

        self.songs[title] = {
            "word frequencies": self._get_word_frequencies(words),
            "lyrics": lyrics,
            "sentiment": self._analyse_sentiment(lyrics),
            "themes": self._analyse_themes(words)
        }

    def process_all_lyrics(self):
        """ Calculate general information about the songs.

        Sum all of the word frequencies from each song. Get the mean
        polarity and subjectivity of the songs. Sum all of the common
        themes and again count them.

        :return: A dictionary containing the above information
        """
        counter = Counter([])
        for key, value in self.songs.items():
            counter += value["word frequencies"]

        polarity = self._get_mean_polarity()
        subjectivity = self._get_mean_subjectivity()

        themes = []
        for key, value in self.songs.items():
            # Build a list of strings from the counted themes
            string_only = [theme[0] for theme in value["themes"]]
            themes.extend(string_only)

        data = {
            "word frequencies": counter.most_common(10),
            "polarity": polarity,
            "subjectivity": subjectivity,
            "theme frequencies": Counter(themes).most_common(5)
        }

        return data
