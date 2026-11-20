import json, os, datetime, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(DATA, "ontology")
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")[:80] or "object"

orgs = json.load(open(os.path.join(DATA, "datagov_organizations.json")))
search = json.load(open(os.path.join(DATA, "harvard_search.json")))

index = []

for o in orgs:
    oid = f"provider:datagov:{o.get('slug')}"
    obj = {
        "id": oid,
        "type": "Provider",
        "name": o.get("name"),
        "source": "data.gov",
        "url": f"https://catalog.data.gov/organization/{o.get('slug')}",
        "organization_type": o.get("organization_type"),
        "aliases": o.get("aliases", []),
        "dataset_count": o.get("dataset_count"),
        "source_count": o.get("source_count"),
        "country": "United States",
        "last_scraped_utc": NOW,
    }
    fname = f"{slugify(oid)}.json"
    with open(os.path.join(OUT, fname), "w") as f:
        json.dump(obj, f, indent=2)
    index.append({"id": oid, "type": "Provider", "file": fname})

for it in search:
    oid = f"dataset:harvard:{it.get('global_id')}"
    obj = {
        "id": oid,
        "type": "Dataset",
        "name": it.get("name"),
        "source": "harvard-dataverse",
        "url": it.get("url"),
        "doi": it.get("global_id"),
        "description": it.get("description"),
        "publisher": it.get("publisher"),
        "authors": it.get("authors", []),
        "producers": it.get("producers", []),
        "contacts": it.get("contacts", []),
        "subjects": it.get("subjects", []),
        "file_count": it.get("fileCount"),
        "created_at": it.get("createdAt"),
        "updated_at": it.get("updatedAt"),
        "published_at": it.get("published_at"),
        "citation": it.get("citation"),
        "last_scraped_utc": NOW,
    }
    fname = f"{slugify(oid)}.json"
    with open(os.path.join(OUT, fname), "w") as f:
        json.dump(obj, f, indent=2)
    index.append({"id": oid, "type": "Dataset", "file": fname})

with open(os.path.join(OUT, "index.json"), "w") as f:
    json.dump({"generated_utc": NOW, "count": len(index), "objects": index}, f, indent=2)
print("objects", len(index), "generated", NOW)
