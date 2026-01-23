import json
import os

# File to update
JSON_FILE = "wiki-count.json"

# Load existing count
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
        current = int(data.get("message", "0"))
else:
    current = 0

# Increment count
new_count = current + 1

# Write updated badge
badge = {
    "schemaVersion": 1,
    "label": "Wiki Visits",
    "message": str(new_count),
    "color": "green"
}

with open(JSON_FILE, "w") as f:
    json.dump(badge, f, indent=2)

print(f"✅ Updated visit count to {new_count}")
