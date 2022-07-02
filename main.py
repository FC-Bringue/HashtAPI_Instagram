import os
from xml.etree.ElementTree import tostring
from dotenv import load_dotenv

import flask
from flask import request, jsonify

from scrape_tool import create_scrape_job
from threading import Thread
load_dotenv()

SCRAPE_LIST = []

app = flask.Flask(__name__)

if os.getenv("PRJ_ENV") == "development":
    app.config["DEBUG"] = True
else:
    app.config["DEBUG"] = False


@app.route('/registerScrape', methods=['GET'])
def register():
    if 'api_key' in request.args:
        api_key = request.args['api_key']
    else:
        return "Error: No APIKEY provided. Please specify."

    if api_key != os.getenv('APIKEY'):
        return "Error: Invalid APIKEY provided."

    if 'hashtag' in request.args:
        hashtag = request.args['hashtag']
    else:
        return "Error: No id field provided. Please specify an id."

    if 'bool' in request.args:
        bool = request.args['bool']
    else:
        return "Error: No id field provided. Please specify a bool."

    needToScrape = open(os.getenv("need_to_scrape_path") +
                        "/need_to_scrape_"+hashtag, 'w')
    needToScrape.write(bool)
    needToScrape.close()

    if bool == "True":
        SCRAPE_LIST.append(hashtag)
        needToScrape = open(os.getenv("need_to_scrape_path") +
                            "/toScrape", 'w')
        needToScrape.write(str(SCRAPE_LIST))
        needToScrape.close()
        thread = Thread(target=create_scrape_job)
        thread.start()
        return "Success: Scrape job created for hashtag: " + hashtag
    else:
        SCRAPE_LIST.remove(hashtag)
        needToScrape = open(os.getenv("need_to_scrape_path") +
                            "/toScrape", 'w')
        needToScrape.write(str(SCRAPE_LIST))
        needToScrape.close()
        thread = Thread(target=create_scrape_job)
        thread.start()
        return "Successfully unregistered scrape job for hashtag: " + hashtag


@app.route('/getHashtag', methods=['GET'])
def hashtag():
    if 'api_key' in request.args:
        api_key = request.args['api_key']
    else:
        return "Error: No APIKEY provided. Please specify."

    if api_key != os.getenv('APIKEY'):
        return "Error: Invalid APIKEY provided."

    if 'hashtag' in request.args:
        hashtag = request.args['hashtag']
    else:
        return "Error: No id field provided. Please specify an id."

    results = open("res/"+hashtag, 'r')
    results = results.read().splitlines()
    results = results[0]
    print(results)
    return jsonify(results)


@app.route('/joebiden', methods=['GET'])
def joebiden():
    return "<h1>DECUDETOIJOE</h1><p>AMOGUS.</p>"


@app.route('/', methods=['GET'])
def home():
    return "<h1>MozeAppHashtagApi</h1><p>AMOGUS.</p>"
