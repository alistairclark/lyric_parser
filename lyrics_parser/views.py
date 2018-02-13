import json

from flask import jsonify
from flask import render_template
from flask import request

from lyrics_parser import app
from lyrics_parser.parser import Parser
from lyrics_parser.song_list_builder import SongListBuilder
from lyrics_parser.helpers import search_genius


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
    id = request.args.get('q', '')
    song_list_builder = SongListBuilder(id)
    data = song_list_builder.fetch_song_data()
    return render_template("results.html", data=data, completed=0)

@app.route("/parse")
def parse():
    total_count = request.values["total_count"]
    completed = request.values["completed"]
    all_lyrics = request.values["all_lyrics"]
    if all_lyrics != "":
        all_lyrics = json.loads(all_lyrics)
    else:
        all_lyrics = []

    url = request.values["url"]

    parser = Parser(all_lyrics)
    parser.get_lyrics(url)

    data = parser.process_lyrics()
    html = render_template(
        "result_data.html",
        data=data,
        completed=completed,
        total_count=total_count
    )

    payload = {
        "html": html,
        "all_lyrics": json.dumps(parser.all_lyrics)
    }

    return jsonify(payload)