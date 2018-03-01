# Lyric Parser

This is a simple Flask app which uses the [Genius API](https://docs.genius.com/) (and some scraping) to analyse the linguistic content of song lyrics.

Search for an artist and Lyric Parser will tell you -
- 10 most commonly used (interesting*) words by the artist
- 5 concepts the artist sings about the most
- Average polarity (positivity/negativity) of the artist's lyrics
- Average subjectivity of the artist's lyrics
- A song by song breakdown of common themes, and a broad sentiment analysis of the song

###### *Excluding the 100 most commonly used English words (and some others that I thought of)

###### N.B. Analysis of common concepts and average polarity/subjectivity is very naive, so should be taken with a pinch of salt 

# Getting started

This project is yet to be deployed, but you can run it locally.

### Prerequisites

You'll need to install [pipenv](https://github.com/pypa/pipenv) and install the requirements for this project

```
pip install pipenv
pipenv --python 3.6
pipenv shell
```

### Installing

You can now run Lyric Parser locally

```
export FLASK_APP=lyrics_parser
flask run
```

# Running the tests

Use [pytest](https://docs.pytest.org/en/latest/) to run the tests

```
pytest
```
