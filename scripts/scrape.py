import json, time, os
import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)

# Data.gov organizations
headers = {"X-Api-Key": "DEMO_KEY"}
r = requests.get("https://api.gsa.gov/technology/datagov/v4/organizations", headers=headers, timeout=60)
r.raise_for_status()
orgs = r.json().get("organizations", [])
with open(os.path.join(DATA, "datagov_organizations.json"), "w") as f:
    json.dump(orgs, f, indent=2)
print("orgs", len(orgs))

# Harvard Dataverse: 500 datasets
items = []
start = 0
per = 100
while len(items) < 500:
    rr = requests.get(
        "https://dataverse.harvard.edu/api/search",
        params={"q": "*", "type": "dataset", "per_page": per, "start": start},
        timeout=60,
    )
    rr.raise_for_status()
    batch = rr.json()["data"]["items"]
    if not batch:
        break
    items.extend(batch)
    start += len(batch)
    time.sleep(0.5)
items = items[:500]
with open(os.path.join(DATA, "harvard_search.json"), "w") as f:
    json.dump(items, f, indent=2)
print("search items", len(items))

# Fetch details
details = []
for i, it in enumerate(items, 1):
    pid = it.get("global_id")
    try:
        rr = requests.get(
            "https://dataverse.harvard.edu/api/datasets/:persistentId",
            params={"persistentId": pid},
            timeout=60,
        )
        rr.raise_for_status()
        details.append(rr.json().get("data"))
    except Exception as e:
        print("ERR", pid, e)
        details.append(None)
    if i % 25 == 0:
        print("details", i)
        time.sleep(1)
    time.sleep(0.2)
with open(os.path.join(DATA, "harvard_details.json"), "w") as f:
    json.dump(details, f, indent=2)
print("details", len(details))
