import json, time, os
import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
items = json.load(open(os.path.join(DATA, "harvard_search.json")))
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; dataset-catalog/1.0)"}
out_path = os.path.join(DATA, "harvard_details.json")
# resume if exists
if os.path.exists(out_path):
    details = json.load(open(out_path))
else:
    details = [None]*len(items)
# ensure length
while len(details) < len(items):
    details.append(None)

for i, it in enumerate(items):
    if details[i] is not None:
        continue
    pid = it.get("global_id")
    try:
        rr = requests.get(
            "https://dataverse.harvard.edu/api/datasets/:persistentId",
            params={"persistentId": pid},
            headers=HEADERS,
            timeout=60,
        )
        if rr.status_code == 200:
            details[i] = rr.json().get("data")
        else:
            print("HTTP", rr.status_code, pid)
            details[i] = {"_error": rr.status_code}
    except Exception as e:
        print("ERR", pid, e)
        details[i] = {"_error": str(e)}
    if (i+1) % 10 == 0:
        with open(out_path, "w") as f:
            json.dump(details, f)
        print("done", i+1)
    time.sleep(0.3)
with open(out_path, "w") as f:
    json.dump(details, f, indent=2)
print("finished", len(details))
