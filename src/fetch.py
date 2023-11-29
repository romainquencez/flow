import feedparser
import json

feeds = []

# read feeds URLs from txt file
txt_file = open("feeds.txt", "r")

for line in txt_file.readlines():
  feed = feedparser.parse(line)
  feeds.append(
    {
      "title": feed.get("title"),
      "link": feed.get("link"),
      "description": feed.get("description"),
      "entries": [
        {
          "title": entry.get("title", ""),
          "link": entry.get("link", ""),
        } for entry in feed.entries
      ]
    }
  )

# dump feeds into a JSON file
with open("_data/feeds.json", "w", encoding="utf-8") as file:
    json.dump(feeds, file, ensure_ascii=False, indent=4)
