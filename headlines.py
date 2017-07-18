import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'sciam': 'http://rss.sciam.com/ScientificAmerican-Global?format=xml',
             'newatlas': 'http://feeds.feedblitz.com/newatlas&x=1',
             'realclear': 'http://www.realclearscience.com/index.xml',
             'livescience': 'http://www.livescience.com/home/feed/site.xml'}


@app.route('/')
@app.route("/<publication>")
def get_news(publication="sciam"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]

    return render_template("home.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
