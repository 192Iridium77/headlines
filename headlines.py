import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib3
import urllib

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

    return render_template("home.html", articles=feed['entries'])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
