from dateutil import parser
import feedparser
import json
import os
import shutil
from slugify import slugify

feeds = []
entries = []
groups = []

# read feeds URLs from txt file
data = json.load(open("feeds.json", "r"))

# iterate on groups
for group in data:
    group_slug = group["slug"]
    group_url = f"{group_slug}.html"
    groups.append(
        {
            "title": group["title"],
            "slug": group_slug,
            "filename": group_url,
        }
    )

    # create page for group
    shutil.copyfile("sample-group.html", group_url)

    # iterate on group's feeds
    for feed in group["feeds"]:
        try:
            data = feedparser.parse(feed)
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
                    "slug": slug,
                    "filename": url,
                    "description": data.feed.get("subtitle"),
                    "image": data.feed.get("logo") or (data.feed.image["href"] if data.feed.get("image") else None),
                    "entries": feed_entries,
                    "group": group_slug,
                }
            )
        
            # create page for feed
            shutil.copyfile("sample-feed.html", url)
        except Exception as error:
            print(f"⚠️ {feed} {error}")
            pass

# sort all entries by date
entries = sorted(entries, key=lambda d: d["date"], reverse=True) 

# delete sample files
os.remove("sample-feed.html")
os.remove("sample-group.html")

# dump feeds into a JSON file
with open("_data/feeds.json", "w", encoding="utf-8") as file:
    json.dump(feeds, file, ensure_ascii=False, indent=4, default=str)

# dump entries into a JSON file
with open("_data/entries.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4, default=str)

# dump groups into a JSON file
with open("_data/groups.json", "w", encoding="utf-8") as file:
    json.dump(groups, file, ensure_ascii=False, indent=4, default=str)
