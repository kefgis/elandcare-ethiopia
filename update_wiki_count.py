import requests
import json
import os

# Repo details
OWNER = "kefgis"
REPO = "elandcare-ethiopia"

# GitHub token from environment
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("❌ No GitHub token found in environment.")
    exit(1)
else:
    print("✅ GitHub token detected.")

# API endpoint
url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
headers = {"Authorization": f"token {TOKEN}"}

# Make request
response = requests.get(url, headers=headers)
print("🔍 API status code:", response.status_code)

if response.status_code != 200:
    print("❌ GitHub API error:", response.text)
    exit(1)

# Parse response
data = response.json()
count = data.get("count", 0)
uniques = data.get("uniques", 0)
print(f"📊 Views: {count}, Unique visitors: {uniques}")

# Write badge JSON
badge = {
    "schemaVersion": 1,
    "label": "Wiki Visits",
    "message": str(count),
    "color": "green"
}

with open("wiki-count.json", "w") as f:
    json.dump(badge, f, indent=2)

print("✅ wiki-count.json updated successfully.")
import requests
import json
import os

# Repo details
OWNER = "kefgis"
REPO = "elandcare-ethiopia"

# GitHub token (must be set in Actions secrets)
TOKEN = os.getenv("GITHUB_TOKEN")

# Output JSON file
JSON_FILE = "wiki-count.json"

def fetch_traffic():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/traffic/views"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("GitHub API error:", response.status_code, response.text)
        exit(1)

    data = response.json()
    return data["count"], data["uniques"]

def update_json(count, uniques):
    badge = {
        "schemaVersion": 1,
        "label": "Wiki Visits",
        "message": str(count),   # total views in last 14 days
        "color": "green"
    }
    with open(JSON_FILE, "w") as f:
        json.dump(badge, f, indent=2)
    print(f"Updated badge: {count} views, {uniques} unique visitors")

if __name__ == "__main__":
    count, uniques = fetch_traffic()
    update_json(count, uniques)
