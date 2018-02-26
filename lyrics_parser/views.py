import json

from flask import jsonify
from flask import render_template
from flask import request

from lyrics_parser.helpers.helpers import search_genius
from lyrics_parser.helpers.parser import Parser
from lyrics_parser.helpers.song_list_builder import SongListBuilder
from lyrics_parser import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    searchword = request.args.get('q', '')
    data = search_genius(searchword)

    return render_template("search.html", data=data)

@app.route("/results")
def results():
    """
    Build list of songs by an artist. Display the results page and begin
    populating it.

    :param id: Genius.com's ID for the artist
    :param artist_name: Name of the artist
    """
    id = request.args.get('artist_id', '')
    artist_name = request.args.get('artist_name', '')
    song_list_builder = SongListBuilder(id)
    data = song_list_builder.get_song_data()

    return render_template(
        "results.html",
        artist_name=artist_name,
        data=data,
        completed=0
    )

@app.route("/parse")
def parse():
    """
    Get the current data from song analysis. Carry out analysis of the current
    song. Update the data.

    :param total_count: The total number of songs to be analysed
    :param completed: The number of songs that have been analysed so far
    :param url: The url of the song to be analysed now
    :param songs: The full dictionary of song data

    :return: Json payload including HTML to be presented on results page
    and the current dictionary of songs.
    """
    total_count = request.values["total_count"]
    completed = request.values["completed"]
    url = request.values["url"]
    songs = request.values["songs"]

    if songs != "":
        songs = json.loads(songs)
    else:
        songs = {}

    parser = Parser(songs)
    parser.add_song(url)

    data = parser.process_all_lyrics()

    html = render_template(
        "result_data.html",
        data=data,
        completed=completed,
        total_count=total_count,
        songs=parser.songs
    )

    payload = {
        "html": html,
        "songs": json.dumps(parser.songs)
    }

    return jsonify(payload)
