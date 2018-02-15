import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from helpers import search_genius
from parser import Parser
from song_list_builder import SongListBuilder


app = Flask(__name__)


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
    id = request.args.get('artist_id', '')
    artist_name = request.args.get('artist_name', '')
    song_list_builder = SongListBuilder(id)
    data = song_list_builder.fetch_song_data()

    return render_template("results.html", artist_name=artist_name, data=data, completed=0)

@app.route("/parse")
def parse():
    total_count = request.values["total_count"]
    completed = request.values["completed"]
    url = request.values["url"]
    all_lyrics = request.values["all_lyrics"]

    if all_lyrics != "":
        all_lyrics = json.loads(all_lyrics)
    else:
        all_lyrics = []

    parser = Parser(all_lyrics)
    parser.get_lyrics(url)
    data = parser.process_lyrics()

    html = render_template(
        "result_data.html",
        data=data,
        completed=completed,
        total_count=total_count
    )

    payload = {"html": html, "all_lyrics": json.dumps(parser.all_lyrics)}

    return jsonify(payload)
