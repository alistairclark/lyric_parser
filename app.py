import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import requests

from song_list_builder import SongListBuilder
from parser import Parser


app = Flask(__name__)

def search_genius(search_term):
    headers = {
        "Authorization": "Bearer {}".format(
            "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa")
    }

    response = requests.get(
        "https://api.genius.com/search?q={}".format(search_term),
        headers=headers
    )

    results = response.json()["response"]["hits"]
    data = {}

    for result in results:
        data[result["result"]["primary_artist"]["id"]] = {
            "name": result["result"]["primary_artist"]["name"],
            "image_url": result["result"]["primary_artist"]["image_url"]
        }

    return data

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
