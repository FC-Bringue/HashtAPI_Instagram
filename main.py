import os
from dotenv import load_dotenv

import flask
from flask import request, jsonify

from instascrape import *
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.addArguments("--disable-gpu")
chromeOptions.addArguments("--no-sandbox")
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

    SESSION_ID = os.getenv("SESSIONID")

    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
               "cookie": "sessionid="+SESSIONID+";"}

    scrape_hashtag = Hashtag(
        'https://www.instagram.com/explore/tags/' + hashtag + '/')
    scrape_hashtag.scrape(headers=headers)

    results = []

    for post in scrape_hashtag.get_recent_posts(20, webdriver=webdriver):
        results.append(post.display_url)

    return jsonify(results)


@app.route('/', methods=['GET'])
def home():
    return "<h1>MozeAppHashtagApi</h1><p>AMOGUS.</p>"
