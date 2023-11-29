import feedparser
import json

feeds = []

# read feeds URLs from txt file
txt_file = open("feeds.txt", "r")

for line in txt_file.readlines():
  data = feedparser.parse(line)
  feeds.append(
    {
      "title": data.feed.title,
      "link": data.feed.link,
      "entries": [
        {
          "title": entry.title,
          "link": entry.link,
          "description": entry.description,
          "date": entry.get("published", entry.get("created", entry.get("updated"))),
          "image": None,
        } for entry in data.entries
      ]
    }
  )

# dump feeds into a JSON file
with open("_data/feeds.json", "w", encoding="utf-8") as file:
    json.dump(feeds, file, ensure_ascii=False, indent=4)
