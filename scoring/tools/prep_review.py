"""One-off: export every hero line plus ability context into review batches for hand review."""
import json, re, html, os, urllib.request, time

os.makedirs("data/review", exist_ok=True)
d = json.load(open("site/data.json", encoding="utf-8"))
heroes = json.load(open("data/heroes.json", encoding="utf-8"))
ids = {h["name"]: h["id"] for h in heroes}

def strip(t):
    t = re.sub(r"<svg.*?</svg>", "", t or "", flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

glossary = {}
for name in d["heroes"]:
    url = f"https://api.deadlock-api.com/v1/assets/items/by-hero-id/{ids[name]}"
    req = urllib.request.Request(url, headers={"User-Agent": "patchnotes-site/1.0"})
    items = json.load(urllib.request.urlopen(req, timeout=60))
    abil = []
    for a in items:
        if a.get("type") != "ability" or a.get("ability_type") == "melee":
            continue
        desc = a.get("description") or {}
        text = " ".join(strip(desc.get(k)) for k in ("desc", "quip") if isinstance(desc, dict) and desc.get(k))
        ups = []
        for i, u in enumerate(a.get("upgrades") or [], 1):
            parts = [f'{p.get("name")} {p.get("bonus")}' for p in u.get("property_upgrades", [])]
            ups.append(f"T{i}: " + ", ".join(parts))
        abil.append({"name": a["name"], "slot": a.get("ability_type"), "description": text[:600], "current_upgrades": ups})
    glossary[name] = abil
    time.sleep(0.05)
json.dump(glossary, open("data/review/ability_glossary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# hero lines not yet hand-reviewed (pass --all to export every line)
import sys
reviewed = {} if "--all" in sys.argv or not os.path.exists("scoring/reviewed_tags.json") else \
    json.load(open("scoring/reviewed_tags.json", encoding="utf-8"))
lines = []
for p in d["patches"]:
    section = ""
    for i, l in enumerate(p["lines"]):
        if l.get("h"):
            section = l["h"]
        if not l.get("hero") or l["t"] in reviewed:
            continue
        lines.append({"id": f'{p["id"]}:{i}', "hero": l["hero"], "patch": p["title"], "date": p["date"],
                      "section": section, "text": l["t"], "auto_tag": l["s"]})

# balance heroes across 8 batches by line count
by_hero = {}
for l in lines:
    by_hero.setdefault(l["hero"], []).append(l)
batches = [[] for _ in range(8)]
for hero, ls in sorted(by_hero.items(), key=lambda kv: -len(kv[1])):
    min(batches, key=len).extend(ls)
for k, b in enumerate(batches, 1):
    b.sort(key=lambda l: (l["hero"], l["date"]))
    json.dump(b, open(f"data/review/batch_{k}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(k, len(b), sorted({l["hero"] for l in b}))
print("total", len(lines))
