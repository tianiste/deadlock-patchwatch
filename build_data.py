"""Builds site/data.json from Steam patch announcements + deadlock-api hero stats.

Re-run to refresh:  python build_data.py  (fetches fresh data)
"""
import json, re, html, datetime, urllib.request, time, sys, collections, os

FETCH = "--offline" not in sys.argv
os.makedirs("data", exist_ok=True)  # raw API downloads (git-ignored)

def get(url, path):
    if FETCH:
        req = urllib.request.Request(url, headers={"User-Agent": "patchnotes-site/1.0"})
        with urllib.request.urlopen(req, timeout=90) as r:
            open(path, "wb").write(r.read())
    return json.load(open(path, encoding="utf-8"))

news = get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1422450&count=1000&maxlength=0&format=json", "data/steam.json")["appnews"]["newsitems"]
heroes = get("https://api.deadlock-api.com/v1/assets/heroes", "data/heroes.json")
since = int(time.time()) - 14 * 86400
stats = get(f"https://api.deadlock-api.com/v1/analytics/hero-stats?min_unix_timestamp={since}", "data/herostats.json")

heroes = [h for h in heroes if h.get("player_selectable") and not h.get("disabled")]
by_id = {h["id"]: h for h in heroes}

# names as they appear in patch notes -> canonical hero name
alias = {}
for h in heroes:
    n = h["name"]
    alias[n.lower()] = n
    if n.startswith("The "):
        alias[n[4:].lower()] = n
alias.update({
    "the magnificent sinclair": "Sinclair", "magnificent sinclair": "Sinclair",
    "geist": "Lady Geist", "mo and krill": "Mo & Krill", "mo & krill": "Mo & Krill",
    "mcginnis": "McGinnis", "greytalon": "Grey Talon", "danny": "Deadman Danny",
    "harrow": "Nurse Harrow", "seven": "Seven", "vindcita": "Vindicta",
})
alias = {k: v for k, v in alias.items() if any(h["name"] == v for h in heroes)}

def clean(text):
    t = text.replace("\\[", "[").replace("\\]", "]")
    t = re.sub(r"\[/?p\]|<p[^>]*>|</p>|<br\s*/?>|\[\*\]|\[/\*\]|<li>|</li>", "\n", t, flags=re.I)
    t = re.sub(r"\[/?[a-z0-9]+(=[^\]]*)?\]", "", t, flags=re.I)  # bbcode tags, keeps [ General ] style headers? handled below
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t)

def clean_keep_headers(text):
    t = text.replace("\\[", "⟦").replace("\\]", "⟧")
    t = re.sub(r"\[/?p\]|<p[^>]*>|</p>|<br\s*/?>|\[\*\]|\[/\*\]|<li>|</li>", "\n", t, flags=re.I)
    t = re.sub(r"\[/?(b|u|i|h\d|list|olist|url[^\]]*|img[^\]]*|strike|spoiler|quote[^\]]*|table|tr|td|th|hr|previewyoutube[^\]]*)\]", "", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("⟦", "[").replace("⟧", "]")
    return html.unescape(t)

# ---------- buff / nerf heuristic ----------
LOWER_IS_BETTER = re.compile(
    r"cooldown|cast time|cast delay|cast point|windup|wind-up|wind up|delay|startup|charge time|"
    r"channel(ing)? time|lockout|reload time|reload duration|spread|recoil|cost|penalty|self[- ]damage|"
    r"time to|ramp[- ]?up time|backswing|recovery|stamina cooldown|respawn|vulnerab|slower|"
    r"debuff on (?:self|him|her)|travel time|arming time|lock-?on time|fuse", re.I)
UP = re.compile(r"\b(increased|increase|increases|raised|buffed|improved|extended|longer|faster|more)\b", re.I)
DOWN = re.compile(r"\b(reduced|reduce|reduces|decreased|decrease|decreases|lowered|nerfed|shorter|slower|less|fewer)\b", re.I)
NUM = r"[-+]?\d*\.?\d+"
FROM_TO = re.compile(r"from\s+\"?([-+]?\d*\.?\d+)[^\s\"]*\"?.*?\bto\s+\"?([-+]?\d*\.?\d+)", re.I)

def classify(change):
    c = change.lower()
    if re.match(r"^(fixed|fix |fixes)", c) or "visual" in c or "tooltip" in c or " vfx" in c or " fx " in c or "sound" in c or "audio" in c or "animation" in c or "model" in c and "hitbox" not in c:
        return 0
    if c.startswith("reworked") or "rescaled" in c or "redistributed" in c:
        return 0
    if re.search(r"changed from|is now \"|now (?:is|works|uses|scales)", c):
        return 0
    nl = re.search(r"\bno longer\b(.*)", c)
    if nl:
        # Removing a drawback is a buff ("no longer does reduced damage to objectives");
        # removing a benefit is a nerf ("no longer grants +10% fire rate").
        lost = nl.group(1)
        if re.search(r"cooldown no longer starts after", c):
            return 1
        if re.search(r"can no longer be (?:destroyed|interrupted|dispelled|cancel|purged|stopped)", c):
            return 1
        if re.search(r"can no longer", c):
            return -1
        # losing a benefit, even if it's worded with "reduce"/"delay" (enemy debuffs, cooldown cuts)
        if re.search(r"reduc\w* (?:its |the |your )?cooldown|-\d[\d.]*s? (?:cooldown|charge delay|delay)|"
                     r"prevents? death|unstoppable|disables? (?:the )?target|reduc\w* (?:enemy|healing|fire rate)|-\d+% \w+ (?:regen )?reduction", lost):
            return -1
        drawback = re.search(
            r"\breduced\b|\bless\b|\blower\b|penal|\bcost|requir|interrupt|\bself\b|self[- ]|yourself|"
            r"\blose|suffer|delay|cancel|\bbreaks?\b|consum|limited|limit the|\bcap\b|capped|minimum|"
            r"cast time|post cast|windup|backswing|brew time|initial|wakes? up|disabled by|goes on cooldown|pause|"
            r"gets? (?:blocked|dispelled|destroyed|stopped|interrupted)|slows? (?:you|him|her|itself|the caster)|"
            r"affected by (?:slow|stun|silence|disarm|cc)|\block|\bstops?\b|prevents? (?:you|him|her|jump|mantl|movement)|restrict|"
            r"(?:hit|damage|knock|pull|stun)s? (?:you|yourself|him|her|allies|teammates)", lost)
        return 1 if drawback else -1
    c_nl = c
    lower_better = bool(LOWER_IS_BETTER.search(c.split(" from ")[0] if " from " in c else c))
    direction = 0
    if UP.search(c_nl) and not DOWN.search(c_nl):
        direction = 1
    elif DOWN.search(c_nl) and not UP.search(c_nl):
        direction = -1
    m = FROM_TO.search(c)
    if m and direction == 0:
        try:
            a, b = abs(float(m.group(1))), abs(float(m.group(2)))
            direction = 1 if b > a else -1 if b < a else 0
        except ValueError:
            pass
    if direction:
        # "reduced from -20% to -10%" style negatives on cooldown reduction bonuses: abs() handles magnitude
        if lower_better:
            direction = -direction
        # damage taken / enemy-favour stats
        if re.search(r"damage taken|enemy|enemies'? (?:resist|heal)", c) and re.search(r"amplif|taken by|resist reduction|slow|stun", c) is None and "damage taken" in c:
            direction = -direction
        return direction
    if re.search(r"\bno longer\b", c):
        return -1 if not re.search(r"no longer (?:has|have|suffers?|loses?|gets? interrupted|interrupt|consumes?|requires?|costs?|penal|slows? (?:you|him|her|self)|self)", c) else 1
    if re.search(r"\bnow also\b|\badditionally\b|\bnow (?:grants|gives|applies|deals|heals|pierces|stuns|silences|ignores|can)\b|\bcan now\b|\badded\b", c):
        return 1
    return 0

ITEM_HEADERS = re.compile(r"item|weapon|vitality|spirit|general|map|misc|hud|ui|bug|matchmaking|ranked|neutral|trooper", re.I)

patches = []
lines_out = []
unknown_prefix = collections.Counter()
for n in sorted(news, key=lambda n: n["date"]):
    if n["feedname"] != "steam_community_announcements":
        continue
    body = clean_keep_headers(n["contents"])
    section = "General"
    hero_lines = 0
    raw_lines = []
    ctx = None
    for raw in body.split("\n"):
        line = raw.strip()
        if not line:
            continue
        hm = re.match(r"^\[\s*([^\]]+?)\s*\]$", line)
        if hm:
            section = hm.group(1).strip()
            ctx = None
            raw_lines.append({"h": section})
            continue
        if not line.startswith("-") and not line.startswith("•"):
            ctx = alias.get(line.rstrip(":").strip().lower())
            raw_lines.append({"h2": ctx} if ctx else {"t": line})
            continue
        line = line.lstrip("-• ").strip()
        m = re.match(r"^([A-Za-z&'. ]{2,30}?)\s*:\s*(.+)$", line)
        hero = None
        if m:
            key = m.group(1).strip().lower()
            hero = alias.get(key)
            if not hero and not ctx and section.lower().startswith("hero"):
                unknown_prefix[m.group(1).strip()] += 1
        rec = {"t": line}
        change = m.group(2).strip() if hero else line
        if not hero and ctx:
            hero = ctx
            rec["t"] = f"{ctx}: {line}"
        if hero:
            score = classify(change)
            rec.update({"hero": hero, "s": score})
            hero_lines += 1
        raw_lines.append(rec)
    if not any(r.get("hero") for r in raw_lines) and len(n["contents"]) < 2500:
        continue  # hero teasers / announcements with no balance content
    date = datetime.datetime.fromtimestamp(n["date"], datetime.UTC)
    patches.append({
        "id": n["gid"], "title": n["title"].strip(), "date": date.strftime("%Y-%m-%d"),
        "url": n["url"], "lines": raw_lines,
    })

stat_rows = []
for s in stats:
    h = by_id.get(s["hero_id"])
    if not h or s["matches"] < 500:
        continue
    stat_rows.append({
        "hero": h["name"], "matches": s["matches"], "wins": s["wins"],
        "kills": s["total_kills"], "deaths": s["total_deaths"], "assists": s["total_assists"],
    })

out = {
    "generated": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"),
    "statsSince": datetime.datetime.fromtimestamp(since, datetime.UTC).strftime("%Y-%m-%d"),
    "heroes": sorted(h["name"] for h in heroes),
    "patches": patches,
    "stats": stat_rows,
}
import os
os.makedirs("site", exist_ok=True)
json.dump(out, open("site/data.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
tot = sum(1 for p in patches for l in p["lines"] if l.get("hero"))
sc = collections.Counter(l["s"] for p in patches for l in p["lines"] if l.get("hero"))
print(f"{len(patches)} patches, {tot} hero lines, scores {dict(sc)}; size {os.path.getsize('site/data.json')//1024}KB")
print("unknown hero-section prefixes:", unknown_prefix.most_common(25))

# ---------- hero icons (site/icons) + per-hero colour ----------
os.makedirs("site/icons", exist_ok=True)
meta = {}
for h in heroes:
    slug = re.sub(r"[^a-z0-9]+", "-", h["name"].lower()).strip("-")
    for kind, key in (("sm", "icon_image_small_webp"), ("card", "icon_hero_card_webp")):
        url, path = (h.get("images") or {}).get(key), f"site/icons/{slug}-{kind}.webp"
        if url and not os.path.exists(path):
            req = urllib.request.Request(url, headers={"User-Agent": "patchnotes-site/1.0"})
            open(path, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    meta[h["name"]] = {"slug": slug, "color": (h.get("colors") or {}).get("style_hex")}
json.dump(meta, open("site/heroes-meta.json", "w"), indent=0)
print(f"icons ready for {len(meta)} heroes")
