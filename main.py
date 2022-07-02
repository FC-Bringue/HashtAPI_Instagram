import os
from dotenv import load_dotenv

import flask
from flask import request, jsonify

from instascrape import *

load_dotenv()

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/getHashtag', methods=['GET'])
def hashtag():
    if 'api_key' in request.args:
        api_key = request.args['api_key']
    else:
        return "Error: No APIKEY provided. Please specify."

    if api_key != os.getenv('TEST'):
        return "Error: Invalid APIKEY provided."

    if 'hashtag' in request.args:
        hashtag = request.args['hashtag']
    else:
        return "Error: No id field provided. Please specify an id."

    scrape_hashtag = Hashtag(
        'https://www.instagram.com/explore/tags/' + hashtag + '/')
    scrape_hashtag.scrape()

    results = []

    for post in scrape_hashtag.get_recent_posts(20):
        results.append(post.display_url)

    return jsonify(results)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


app.run()
