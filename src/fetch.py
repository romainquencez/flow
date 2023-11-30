from dateutil import parser
import feedparser
import json
import os
import shutil
from slugify import slugify

feeds = []
entries = []

# read feeds URLs from txt file
txt_file = open("feeds.txt", "r")

for line in txt_file.readlines():
    data = feedparser.parse(line)
    slug = slugify(data.feed.title)
    url = f"{slug}.html"

    feed_entries = []

    # add entries
    for entry in data.entries:
        # get publication date
        published_on = (
            entry.get("published")
            or entry.get("created")
            or entry.get("updated")
        )
        published_on_parsed = None
        if published_on is not None:
            try:
                published_on_parsed = parser.parse(published_on, fuzzy=True)
            except (TypeError, parser.ParserError):
                pass
    
        feed_entry = {
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "date": published_on_parsed,
            "image": entry.enclosures[0].href if len(entry.enclosures) else None,
            "feed": {
              "title": data.feed.title,
            },
        }
        entries.append(feed_entry)
        feed_entries.append(feed_entry)

    # add feed
    feeds.append(
        {
            "title": data.feed.title,
            "link": data.feed.link,
            "filename": url,
            "description": data.feed.subtitle,
            "image": data.feed.get("logo") or (data.feed.image["href"] if data.feed.get("image") else None),
        }
    )

    # create page for feed
    shutil.copyfile("sample-feed.html", url)

# delete sample-feed file
os.remove("sample-feed.html")

# dump feeds into a JSON file
with open("_data/feeds.json", "w", encoding="utf-8") as file:
    json.dump(feeds, file, ensure_ascii=False, indent=4)

# dump entries into a JSON file
with open("_data/entries.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4)
