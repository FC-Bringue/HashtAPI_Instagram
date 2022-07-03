import json
import codecs
import json
import os
import ast
from time import sleep
from dotenv import load_dotenv
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError
from postgre import fetchData, getHashtagList, saveData

load_dotenv()


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


def getApiClient():
    device_id = None
    try:
        settings_file = os.getenv("settings_path")
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                os.getenv("usrnme"), os.getenv("psswrd"),
                on_login=lambda x: onlogin_callback(x, os.getenv("settings_path")))
            return api
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                os.getenv("usrnme"), os.getenv("psswrd"),
                settings=cached_settings)
            return api

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print(
            'ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            os.getenv("usrnme"), os.getenv("psswrd"),
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, os.getenv("settings_path")))
        return api

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(
            e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)


def create_scrape_job():
    while True:
        if os.getenv("PRJ_ENV") == "development":
            toScrape = open(os.getenv("need_to_scrape_path") +
                            "/toScrape", 'r').read().splitlines()
            toScrape = toScrape[0]
            print("toScrape: " + toScrape)
            toScrape = ast.literal_eval(toScrape)
        else:
            toScrape = getHashtagList()
            print("toScrape: " + str(toScrape))
        for scrape in toScrape:
            scrape = scrape[0]
            if os.getenv("PRJ_ENV") == "development":
                needToScrape = open(os.getenv("need_to_scrape_path") +
                                    "/need_to_scrape_"+scrape, 'r')
                needToScrape = needToScrape.read().splitlines()
                needToScrape = needToScrape[0]
                print(needToScrape)
                if needToScrape == "False":
                    print("No scrape job")
                if needToScrape == "True":
                    api = getApiClient()
                    res = api.tag_section(scrape, 'recent')
                    with open("res/"+scrape, 'w') as outfile:
                        json.dump(res, outfile, default=to_json)
                        print('SAVED: ' + scrape)
            else:
                api = getApiClient()
                # print(scrape)
                #print("scrape :" + scrape)
                #print(type(api.tag_section(scrape, 'recent')))
                res = api.tag_section(scrape, 'recent')
                res = json.dumps(res)
                #print("res: " + str(res))
                toSave = saveData(res, scrape)
                #print("toSave :" + str(toSave))
            print("Scrape job done")
        sleep(int(os.getenv("refresh_data_frequency")))
