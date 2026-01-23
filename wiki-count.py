import json
import os

JSON_FILE = "wiki-count.json"

def update_visit_count():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {
            "schemaVersion": 1,
            "label": "Wiki Visits",
            "message": "0",
            "color": "green"
        }

    current_count = int(data["message"])
    data["message"] = str(current_count + 1)

    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Updated visit count to {data['message']}")

if __name__ == "__main__":
    update_visit_count()
