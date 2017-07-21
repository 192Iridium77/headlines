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


@app.route('/')
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "newatlas"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Adelaide,AU")

    return render_template("home.html", articles=feed['entries'], weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=83eeda99c5495de62d6086f706f7f1bf"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]
        }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
