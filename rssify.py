import os
import tomllib
from datetime import datetime

import requests
from rfeed import Feed, Guid, Item
from bs4 import BeautifulSoup
from flask import Flask

class Scraper:
    def __init__(self, name: str, desc: str, url: str, body: str, title: str, link: str, date: str):
        self.name = name
        self.desc = desc
        self.url = url
        self.body = body
        self.title = title
        self.link = link
        self.date = date

    def scrape(self) -> None|list:
        page = Scraper.get_page(self.url)
        if not page:
            return None

        posts = []
        for post in page.select(self.body)[:10]:
            title = post.select_one(self.title).text.strip()
            link = post.select_one(self.link).attrs["href"]
            date = post.select_one(self.date).text.strip()

            posts.append({
                "title": title,
                "link": link,
                "description": title,
                "author": "Noah",
                "date": date,
            })

        return posts

    def rss(self) -> None|str:
        posts = self.scrape()
        if not posts:
            return None
        pass

        items = []
        for post in posts:
            items.append(Item(
                title=post["title"],
                link=post["link"],
                description=post["title"],
                author="Noah",
                guid=Guid(post["link"]),
                pubDate=datetime.strptime(post["date"], "%Y-%m-%d"),
            ))

        feed = Feed(
            title=self.name,
            link = self.url,
            description = self.desc,
            language = "en-US",
            lastBuildDate = datetime.now(),
            items = items,
        )

        return feed.rss()

    @classmethod
    def get_page(cls, url: str) -> None|BeautifulSoup:
        r = requests.get(url)
        if not r.ok:
            return None
        return BeautifulSoup(r.text, "html.parser")

# SCRAPERS

scrapers = {}

def load_scrapers(path: str):
    with open(path, "rb") as f:
        data = tomllib.load(f)
        for id, config in data.items():
            scrapers[id] = Scraper(
                name=config.get("name"),
                desc=config.get("description", config.get("name")),
                url=config.get("url"),
                body=config.get("body"),
                title=config.get("title"),
                link=config.get("link"),
                date=config.get("date"),
            )

# APP

app = Flask(__name__)

@app.route("/<path:id>")
@app.errorhandler(404)
@app.errorhandler(500)
def rssify(id):
    if id not in scrapers:
        return "", 404

    scraper = scrapers[id]
    feed = scraper.rss()
    if not feed:
        return "", 500

    return feed

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1111))

    load_scrapers("feeds.toml")

    app.run(host='0.0.0.0', port=port)
