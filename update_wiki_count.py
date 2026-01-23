import requests
import json
import os

# Repo details
OWNER = "kefgis"
REPO = "elandcare-ethiopia"

# GitHub token (store securely in GitHub Actions secrets)
TOKEN = os.getenv("GITHUB_TOKEN")

# Output JSON file
JSON_FILE = "wiki-count.json"

def fetch_traffic():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}, {response.text}")

    data = response.json()
    return data["count"], data["uniques"]

def update_json(count, uniques):
    badge = {
        "schemaVersion": 1,
        "label": "Wiki Visits",
        "message": str(count),
        "color": "green"
    }
    with open(JSON_FILE, "w") as f:
        json.dump(badge, f, indent=2)
    print(f"Updated badge: {count} views, {uniques} unique visitors")

if __name__ == "__main__":
    count, uniques = fetch_traffic()
    update_json(count, uniques)
