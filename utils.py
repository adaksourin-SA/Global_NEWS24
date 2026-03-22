import os
import json
from urllib.request import urlopen, Request
from PIL import Image

CACHE_DIR = "cache"
BOOKMARK_FILE = "bookmarks.json"

os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_and_cache_image(url, index):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)

        path = os.path.join(CACHE_DIR, f"img_{index}.jpg")

        with urlopen(req) as response, open(path, 'wb') as f:
            f.write(response.read())

        img = Image.open(path)

        if img.mode in ["RGBA", "P"]:
            img = img.convert("RGB")

        img.thumbnail((200, 184))
        img.save(path)

        return path
    except:
        return None

def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    return []

def save_all_bookmarks(data):
    with open(BOOKMARK_FILE, "w") as f:
        json.dump(data, f, indent=4)

def toggle_bookmark(article):
    data = load_bookmarks()

    # Check if already bookmarked (by URL)
    exists = any(item["url"] == article["url"] for item in data)

    if exists:
        # Remove bookmark
        data = [item for item in data if item["url"] != article["url"]]
        save_all_bookmarks(data)
        return False  # now unbookmarked
    else:
        data.append(article)
        save_all_bookmarks(data)
        return True   # now bookmarked

def is_bookmarked(article):
    data = load_bookmarks()
    return any(item["url"] == article["url"] for item in data)