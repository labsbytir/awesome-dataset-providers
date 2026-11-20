import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

orgs = json.load(open(os.path.join(DATA, "datagov_organizations.json")))
search = json.load(open(os.path.join(DATA, "harvard_search.json")))

FIELDS = ["Provider","Sets","Total Datasets","URL","Category","Country","State or territory","Description","Target Users","License Type","Publisher","Researchers","Formats","Commercial Use Policy","Attribution Policy","doi.org","UNF","Citation","Contact Owner","Subject of dataset","Keywords","Topic Classification","Languages","Funding Information","Depositor","Deposit Date","Date of collection","Datatype","Method of collection","Geospatial Meta Fields"]

def blank_record(provider=""):
    return {k: "" for k in FIELDS} | {"Provider": provider}

# Providers
providers = []
for o in orgs:
    rec = blank_record(o.get("name",""))
    rec["Sets"] = "data.gov organization"
    rec["Total Datasets"] = o.get("dataset_count")
    rec["URL"] = f"https://catalog.data.gov/organization/{o.get('slug')}"
    rec["Category"] = o.get("organization_type","")
    rec["Country"] = "United States"
    rec["Publisher"] = o.get("name","")
    providers.append(rec)

# Datasets
datasets = []
for it in search:
    rec = blank_record(it.get("publisher",""))
    rec["Sets"] = it.get("name","")
    rec["Total Datasets"] = it.get("fileCount")
    rec["URL"] = it.get("url","")
    rec["Category"] = ", ".join(it.get("subjects",[]) or [])
    rec["Country"] = ""
    rec["Description"] = it.get("description","")
    rec["Publisher"] = it.get("publisher","")
    rec["Researchers"] = ", ".join(it.get("authors",[]) or it.get("producers",[]) or [])
    rec["doi.org"] = it.get("global_id","")
    rec["Citation"] = it.get("citation","")
    contacts = it.get("contacts",[]) or []
    rec["Contact Owner"] = "; ".join([f"{c.get('name','')} <{c.get('email','')}>" if False else c.get("name","") for c in contacts if c.get("name")])
    rec["Subject of dataset"] = ", ".join(it.get("subjects",[]) or [])
    rec["Keywords"] = ", ".join(it.get("subjects",[]) or [])
    rec["Topic Classification"] = ", ".join(it.get("subjects",[]) or [])
    rec["Deposit Date"] = it.get("createdAt","")
    rec["Datatype"] = "dataset"
    datasets.append(rec)

with open(os.path.join(DATA,"providers.json"),"w") as f:
    json.dump(providers, f, indent=2)
with open(os.path.join(DATA,"datasets.json"),"w") as f:
    json.dump(datasets, f, indent=2)

# README
lines = []
lines.append("# Awesome Dataset Providers")
lines.append("")
lines.append("Curated list of dataset providers and datasets.")
lines.append("")
lines.append(f"- Data.gov organizations: {len(providers)}")
lines.append(f"- Harvard Dataverse datasets: {len(datasets)} (crawled first 500)")
lines.append("")
lines.append("## Data.gov Providers")
lines.append("")
lines.append("| Provider | Type | Total Datasets | URL |")
lines.append("|---|---|---:|---|")
for p in providers:
    lines.append(f"| {p['Provider']} | {p['Category']} | {p['Total Datasets']} | {p['URL']} |")
lines.append("")
lines.append("## Harvard Dataverse Datasets (first 500)")
lines.append("")
lines.append("| Dataset | Publisher | Subjects | DOI | Created |")
lines.append("|---|---|---|---|---|")
for d in datasets:
    lines.append(f"| {d['Sets']} | {d['Publisher']} | {d['Subject of dataset']} | {d['doi.org']} | {d['Deposit Date']} |")
lines.append("")
lines.append("Detailed metadata: `data/providers.json`, `data/datasets.json`.")
with open(os.path.join(BASE,"README.md"),"w") as f:
    f.write("\n".join(lines)+"\n")
print("done", len(providers), len(datasets))
