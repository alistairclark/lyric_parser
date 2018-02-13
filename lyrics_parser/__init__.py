from flask import Flask


app = Flask(__name__)

import lyrics_parser.views
