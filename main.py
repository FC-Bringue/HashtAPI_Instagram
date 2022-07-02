from instascrape import Profile, scrape_posts
import os
from dotenv import load_dotenv

import flask
from flask import request, jsonify

from instascrape import *
from selenium import webdriver
from selenium.webdriver import Chrome
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

webdriver = Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), options=chromeOptions)

load_dotenv()

app = flask.Flask(__name__)

if os.getenv("FLASK_ENV") == "development":
    app.config["DEBUG"] = True
else:
    app.config["DEBUG"] = False


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

    scrape_hashtag = Hashtag(
        'https://www.instagram.com/explore/tags/' + hashtag + '/')
    scrape_hashtag.scrape()

    results = []

    for post in scrape_hashtag.get_recent_posts(20):
        results.append(post.display_url)

    return jsonify(results)


@app.route('/joebiden', methods=['GET'])
def joebiden():
    return "<h1>DECUDETOIJOE</h1><p>AMOGUS.</p>"


@app.route('/', methods=['GET'])
def home():
    return "<h1>MozeAppHashtagApi</h1><p>AMOGUS.</p>"
