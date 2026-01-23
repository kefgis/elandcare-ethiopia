import requests
import json
import os

OWNER = "kefgis"
REPO = "elandcare-ethiopia"
TOKEN = os.getenv("GITHUB_TOKEN")   # GitHub token stored in Actions secrets
JSON_FILE = "wiki-count.json"

def fetch_traffic():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["count"], data["uniques"]

def update_json(count, uniques):
    badge = {
        "schemaVersion": 1,
        "label": "Wiki Visits",
        "message": str(count),   # this is what changes!
        "color": "green"
    }
    with open(JSON_FILE, "w") as f:
        json.dump(badge, f, indent=2)
    print(f"Updated badge: {count} views, {uniques} unique visitors")

if __name__ == "__main__":
    count, uniques = fetch_traffic()
    update_json(count, uniques)
