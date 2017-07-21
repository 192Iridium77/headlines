import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib
import urllib.parse
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS = {'sciam': 'http://rss.sciam.com/ScientificAmerican-Global?format=xml',
             'newatlas': 'http://feeds.feedblitz.com/newatlas&x=1',
             'realclear': 'http://www.realclearscience.com/index.xml',
             'livescience': 'http://www.livescience.com/home/feed/site.xml'}

DEFAULTS = {'publication':'newatlas',
            'city': 'Adelaide,AU',
            'currency_from':'AUD',
            'currency_to':'USD'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=83eeda99c5495de62d6086f706f7f1bf"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=bc76ca2f0901456faf42a2fdaded3e99"


@app.route('/')
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather data
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency exchange data
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)

    return render_template("home.html", articles=articles, weather=weather, currency_from=currency_from
                           , currency_to=currency_to, rate=rate)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']


def get_weather(query):
    api_url = WEATHER_URL
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urlopen(url).read().decode('utf-8')
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   "country":parsed['sys']['country']
        }
    return weather


def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read().decode("utf-8")

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return to_rate / frm_rate


if __name__ == '__main__':
    app.run(port=5000, debug=True)
