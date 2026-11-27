# Deadlock Patchwatch

Every Deadlock hero buff and nerf from every official patch, with a running buff score for each hero and a win-rate tier list.

Fan-made. Not affiliated with Valve.

## What's in it

- **Heroes**: sortable table of buffs, nerfs, net buff score, win rate and pick rate. Click a hero to see every change made to them, patch by patch, with a chart of their running buff score.
- **Tier list**: S to F tiers by recent win rate, by net buffs, or a mix of both.
- **Patch notes**: full notes for each patch, filterable by hero or search text.
- **Count changes since**: limits every view to patches after a date you pick.

Each hero change is tagged +1 (buff), −1 (nerf) or 0 automatically from its wording. The rules are in `classify()` in `build_data.py`. Wrong tags can be corrected on the page by clicking them (saved in your browser only).

## Data sources

- Patch notes: official Deadlock announcements from the [Steam news API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1422450&count=1000&maxlength=0), November 2024 onward. Earlier and some forum-only patches are not included.
- Hero list, portraits and win rates: the community [Deadlock API](https://deadlock-api.com). Win rates cover the last 14 days, all ranks.

## Run it locally

The site is static files in `site/`. It loads `data.json` with `fetch`, so serve it rather than opening the file directly:

```
python -m http.server 8765 -d site
```

Then open http://localhost:8765.

## Refresh the data

```
python build_data.py
```

This downloads the latest patches, hero list and win rates, rewrites `site/data.json` and `site/heroes-meta.json`, and downloads portraits for any new heroes into `site/icons/`. Use `python build_data.py --offline` to rebuild from the last downloads in `data/` without fetching.
