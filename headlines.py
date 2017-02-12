import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'sciam': 'http://rss.sciam.com/ScientificAmerican-Global?format=xml',
             'newatlas': 'http://feeds.feedblitz.com/newatlas&x=1',
             'realclear': 'http://www.realclearscience.com/index.xml',
             'livescience': 'http://www.livescience.com/home/feed/site.xml'}

@app.route('/')
@app.route("/<publication>")

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]

    return """<html>
        <body>
            <h1>Headlines</h1>
            <b>{0}</b><br>
            <i>{1}</i><br>
            <p>{2}</p><br>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)