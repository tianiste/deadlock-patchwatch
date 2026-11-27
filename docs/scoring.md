# Scoring rules

How Deadlock Patchwatch turns patch lines into buffs, nerfs, a running score, win-rate shifts and tiers.
Change these rules only with a note here.

## Which lines count

- Source: Valve's official announcements in the Steam news API
  (`ISteamNews/GetNewsForApp`, app 1422450, feed `steam_community_announcements`), checked 2026-11-27.
  Posts with no hero lines and under 2,500 characters (hero teasers, event posts) are skipped.
- A line is a hero change when it starts with a known hero name followed by a colon
  (`- Abrams: ...`), or sits under a bare hero-name line in older posts. Names go through the
  `alias` map in `build_data.py`.
- Item, map and general lines are shown in the patch notes but never scored.

## Tag per line

Each hero line gets +1 (buff), −1 (nerf) or 0 (neither / unclear). The question is always:
after this change, is this hero stronger, weaker, or neither?

1. **Hand-reviewed tags win.** `scoring/reviewed_tags.json` maps each line's exact text to its
   reviewed tag and a short reason. Lines in it show a solid tag on the site.
2. **Everything else falls back to `classify()`** in `build_data.py` (new patches until they're
   reviewed). Those show a dashed tag.

### How the reviewed tags were made (2026-11-27, all 2,582 hero lines)

1. Lines were grouped by hero into 8 batches (`scoring/tools/prep_review.py`), each with every
   ability's current description and T1/T2/T3 upgrades from the Deadlock API as context.
2. **Review A:** 8 reviewers judged every line, seeing the automatic tag as a hint.
3. **Review B:** 8 more reviewers judged every line blind, without the automatic tag, so they
   couldn't anchor on it.
4. Where A and B agreed (2,482 lines, 96.1%), that tag is final.
5. The 100 disagreements went to 4 judges, who saw both reasons, the automatic tag, the ability
   descriptions and the hero's other lines from the same patch. Their call is final
   (`scoring/tools/merge_reviews.py`).
6. Identical line text appearing in more than one patch was checked: no conflicting tags.

Standard used by every reviewer:
- Higher is better: damage, scaling, health, regen, range, radius, own effect duration, charges,
  speed, fire rate, ammo, resists, lifesteal, barrier, healing.
- Lower is better: cooldown, cast/wind-up/charge/arm/deploy time, time between charges, cost,
  self-damage, penalties on the hero, enemy counterplay windows.
- Debuffs on enemies getting stronger or longer are buffs. On upgrades, "−20s" is cooldown
  reduction, so a bigger negative number is a buff.
- "No longer" removing a drawback is a buff; removing a benefit is a nerf.
- Upgrade swaps ("changed from X to Y") are ±1 only when one side is clearly stronger.
- Fixes, visuals, sound, VO and HUD are 0 unless the fix plainly changes power
  ("fixed not dealing damage" = buff, "fixed dealing bonus damage twice" = nerf).
- Mixed changes are 0 unless the net is clearly one way. Valve's own notes ("same overall
  damage", "~4% DPS nerf") count as strong evidence. Genuinely unclear = 0, never a guess.

Result: 1,056 buffs, 955 nerfs, 571 neutral. The reviewed tags differ from the automatic rules on
333 lines (13%).

### Accuracy checks

| Check | Lines | Agreement |
|-------|-------|-----------|
| Review A vs blind review B | 2,582 | 96.1% identical |
| Final tags vs my own earlier hand-judged holdout sample (seed 7331, debatable line excluded) | 49 | 48; the one difference ("fixed dealing bonus multiple times") is a nerf under the standard, so the final tag is right |
| Spot check of 30 lines where both reviewers overruled the automatic rule | 30 | all 30 judged correct |
| Automatic rules alone, fresh holdout before any tuning | 50 | 44 right, 1 debatable, 5 wrong |

Lines that stay genuinely debatable are tagged 0 with the reason recorded, for example Celeste's
gravity changes, "Life Drain is no longer cancellable", and McGinnis's turret DPS rescale (weaker
below 200 spirit power, stronger above).

### Automatic rules (`classify()`), used only for unreviewed lines

1. **Neutral:** fixes, visual, tooltip, sound, volume, voice-over, animation and model changes;
   HUD, icon, cast-bar and "updated effects" changes; reworks, rescales and redistributions;
   "is now ...", "now works/uses". "Changed from X to Y" is neutral unless Y is just a number.
2. **"No longer" lines:** removing a drawback is +1, removing a benefit is −1, with special cases
   for "can no longer be destroyed/interrupted" (+1) and "cooldown no longer starts after" (+1).
3. **Up or down:** increased/reduced words or the numbers in "from A to B", flipped for
   lower-is-better stats (cooldown, cast time, delay, cost, spread, recoil, penalty, self-damage,
   reload/deploy/arm time, time between charges).
4. Half damage = −1; "now also/grants/applies/deals", "can now", "added" = +1; "same overall" = 0;
   "now only" limiting a drawback = +1; "starts on cooldown" and "now has −X% resist" = −1;
   "now slows your", "now costs/requires/only", "now breaks", "can only" = −1;
   "now starts/scales/allows/causes/has/reflects", "allows", "again" = +1; anything else 0.

Known weak spot (found by the review): T1/T2/T3 lines like "cooldown increased from −18s to −20s"
are read backwards by the automatic rules. New patches should be reviewed, not left to the rules.

### Reviewing a new patch

1. `python build_data.py`, then `python scoring/tools/prep_review.py` (writes batches of all hero
   lines to `data/review/`; only lines missing from `reviewed_tags.json` need review).
2. Two independent reviews (one blind), judge the disagreements, then
   `python scoring/tools/merge_reviews.py --final` to rewrite `scoring/reviewed_tags.json`.
3. Rebuild and commit.

Every line counts the same, so a 1% tweak and a big rework weigh equally. Viewers can override a
tag on the page; overrides stay in that browser's localStorage.

## Change size per line

When a line gives one clean number pair ("from 48s to 42s", same unit, no other stat named in
between) or "increased/reduced by X%", the site shows how much the listed number moved as a % of
its old size (`magnitude()` in `build_data.py`), e.g. "−13%". It's the change in Valve's number,
not a claim about overall power. 1,160 of 2,582 hero lines have one. Upgrade swaps and multi-stat
lines have none.

## Hero numbers

- **Net buffs** = buffs − nerfs over the patches on or after the "Count changes made since" date.
- **Running buff score** = the cumulative net per patch that touched the hero.
- **Win rate** = wins / matches over the last 14 days from `api.deadlock-api.com/v1/analytics/hero-stats`.
  With no rank picked it uses all matches (including unranked ones). Picking one or more of the
  11 major ranks (Initiate ... Eternus, from `/v1/assets/ranks`) adds up those ranks' matches,
  fetched per rank with `min_average_badge=tier*10` and `max_average_badge=tier*10+9` (the match's
  average rank; badge = tier × 10 + subrank). Shown steadied: (wins + 1,000 × average) / (matches + 1,000), so a
  hero with few matches is pulled toward the average. The table's tooltip shows the raw rate and
  match count.
- **Pick rate** = hero matches / all hero matches × 12 (12 heroes per match).
- **Win rate before and after a patch:** for every patch that changed heroes, the all-ranks win
  rate in up to 7 days before vs up to 7 days after, each window clipped at the neighbouring hero
  patches and at today. Windows under a day are skipped, and a hero needs 300+ matches on both
  sides to be shown. Other patches, items and meta shifts also move win rates, so this shows what
  happened after a patch, not proof of what the patch caused.

## Tiers

Each hero's value is turned into a z-score (distance from the average in standard deviations):

- Win rate mode: z of steadied win rate for the chosen rank group. Both mode: 0.7 × z(win rate)
  + 0.3 × z(net buffs). Net buffs mode: z of net buffs over the selected range.
- Cut-offs: S ≥ 1.25, A ≥ 0.5, B ≥ −0.1, C ≥ −0.7, D ≥ −1.3, otherwise F.
- Heroes without a win rate are left out of the win-rate and both modes.
