import feedparser
import json
import shutil
from slugify import slugify

feeds = []
entries = []

# read feeds URLs from txt file
txt_file = open("feeds.txt", "r")

for line in txt_file.readlines():
    data = feedparser.parse(line)
    slug = slugify(data.feed.title)

    # add entries
    for entry in data.entries:
        entries.append(
            {
                "title": entry.title,
                "link": entry.link,
                "description": entry.description,
                "date": entry.get("published", entry.get("created", entry.get("updated"))),
                "image": None,
                "feed": {
                  "title": data.feed.title,
                }
            }
        )

    # add feed
    feeds.append(
        {
            "title": data.feed.title,
            "link": data.feed.link,
            "slug": slug,
        }
    )

    # create page for feed
    shutil.copyfile("sample-feed.html", f"{slug}.html")

# dump feeds into a JSON file
with open("_data/feeds.json", "w", encoding="utf-8") as file:
    json.dump(feeds, file, ensure_ascii=False, indent=4)

# dump entries into a JSON file
with open("_data/entries.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4)
