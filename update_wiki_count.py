#!/usr/bin/env python3
"""
Fetch repository traffic views and write a simple shields-style JSON badge.

Note: The GitHub traffic API endpoint used here (/repos/:owner/:repo/traffic/views)
returns repository view counts (last 14 days). GitHub does not provide a separate
public API for wiki view counts.
"""
import json
import os
import sys
from typing import Tuple

import requests
from requests import RequestException

OWNER = "kefgis"
REPO = "elandcare-ethiopia"
JSON_FILE = os.getenv("OUTPUT_JSON", "wiki-count.json")  # override in env if desired
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_traffic(owner: str, repo: str, token: str) -> Tuple[int, int]:
    if not token:
        print("❌ No GitHub token found in environment (GITHUB_TOKEN).", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/views"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "update-wiki-count-script"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except RequestException as exc:
        print("❌ Request to GitHub API failed:", exc, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except ValueError:
        print("❌ Failed to parse JSON response from GitHub API.", file=sys.stderr)
        sys.exit(1)

    count = int(data.get("count", 0))
    uniques = int(data.get("uniques", 0))
    return count, uniques

def write_badge(path: str, count: int, uniques: int) -> None:
    badge = {
        "schemaVersion": 1,
        "label": "Wiki Visits",
        "message": str(count),
        "color": "green",
        # optional metadata:
        "meta": {
            "uniques": uniques
        }
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(badge, f, indent=2)
    except OSError as exc:
        print(f"❌ Failed to write {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"✅ Updated {path}: {count} views, {uniques} unique visitors")

def main():
    count, uniques = fetch_traffic(OWNER, REPO, TOKEN)
    write_badge(JSON_FILE, count, uniques)

if __name__ == "__main__":
    main()
