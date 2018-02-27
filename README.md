# Lyric Parser

This is a simple Flask app which uses the [Genius API](https://docs.genius.com/) (and some scraping) to analyse the linguistic content of song lyrics.

Search for an artist and Lyric Parser will tell you -
- 10 most commonly used (interesting*) words by the artist
- 5 concepts the artist sings about the most
- Average polarity (positivity/negativity) of the artist's lyrics
- Average subjectivity of the artist's lyrics
- A song by song breakdown of common themes, and a broad sentiment analysis of the song


###### *Excluding the 100 most commonly used English words (and some others that I thought of)

###### N.B. Analysis of common concepts and average polarity/subjectivity is *very* naive, so should be taken with a pinch of salt 
