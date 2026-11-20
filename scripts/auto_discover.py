import os, json, datetime, requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
queries = ["dataset providers", "open data repository", "research data repository", "government open data portal"]

results = []
seen = set()

def add(item):
    url = item.get("url") or item.get("link")
    if not url or url in seen:
        return
    seen.add(url)
    results.append({
        "title": item.get("title"),
        "url": url,
        "snippet": item.get("snippet") or item.get("description") or "",
        "source_engine": item.get("_engine"),
        "last_collected_utc": NOW,
    })

# SearXNG
sx = os.getenv("SEARXNG_URL")
if sx:
    for q in queries:
        try:
            r = requests.get(f"{sx.rstrip('/')}/search", params={"q": q, "format": "json"}, timeout=30)
            r.raise_for_status()
            for it in r.json().get("results", []):
                it["_engine"] = "searxng"
                add(it)
        except Exception as e:
            print("searxng err", e)

# Brave
brave_key = os.getenv("BRAVE_API_KEY")
if brave_key:
    for q in queries:
        try:
            r = requests.get("https://api.search.brave.com/res/v1/web/search", params={"q": q}, headers={"X-Subscription-Token": brave_key, "Accept": "application/json"}, timeout=30)
            r.raise_for_status()
            for it in r.json().get("web", {}).get("results", []):
                it["_engine"] = "brave"
                it["url"] = it.get("url")
                it["snippet"] = it.get("description")
                add(it)
        except Exception as e:
            print("brave err", e)

# SerpAPI engines
serp_key = os.getenv("SERPAPI_API_KEY")
engines = ["bing", "duckduckgo", "google", "google_scholar", "google_light"]
if serp_key:
    for eng in engines:
        for q in queries:
            try:
                params = {"engine": eng, "q": q, "api_key": serp_key}
                r = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
                r.raise_for_status()
                data = r.json()
                for key in ("organic_results", "results"):
                    for it in data.get(key, []) or []:
                        it["_engine"] = f"serpapi:{eng}"
                        it["url"] = it.get("link") or it.get("url")
                        it["snippet"] = it.get("snippet") or it.get("description")
                        add(it)
            except Exception as e:
                print("serpapi", eng, e)

with open(os.path.join(DATA, "discovered_providers.json"), "w") as f:
    json.dump({"generated_utc": NOW, "count": len(results), "results": results}, f, indent=2)
print("discovered", len(results))
