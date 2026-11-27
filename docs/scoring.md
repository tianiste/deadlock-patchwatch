# Scoring rules

How Deadlock Patchwatch turns patch lines into buffs, nerfs, a running score and tiers.
Change these rules only with a note here.

## Which lines count

- Source: Valve's official announcements in the Steam news API
  (`ISteamNews/GetNewsForApp`, app 1422450, feed `steam_community_announcements`), checked 2026-11-27.
  Posts with no hero lines and under 2,500 characters (hero teasers, event posts) are skipped.
- A line is a hero change when it starts with a known hero name followed by a colon
  (`- Abrams: ...`), or sits under a bare hero-name line in older posts. Names go through the
  `alias` map in `build_data.py`.
- Item, map and general lines are shown in the patch notes but never scored.

## Tag per line (`classify()` in `build_data.py`)

Each hero line gets +1 (buff), −1 (nerf) or 0 (neutral), in this order:

1. **Neutral:** fixes, visual, tooltip, sound, volume, voice-over, animation and model changes;
   HUD, icon, cast-bar and "updated effects" changes; reworks, rescales and redistributions;
   "is now ...", "now works/uses". "Changed from X to Y" is neutral (an upgrade swapped for a
   different one) unless Y is just a number, which means the same stat changed and is compared.
2. **"No longer" lines:** removing a drawback is +1 (reduced damage, penalties, costs, cast
   time, delays, interruptions, self-damage, minimum lifetimes, wake-ups, being disabled), removing a
   benefit is −1 (damage, cooldown cuts, enemy debuffs, unstoppable, death prevention).
   "Can no longer be destroyed/interrupted/dispelled" is +1; any other "can no longer" is −1.
   "Cooldown no longer starts after the ability ends" is +1.
3. **Up or down:** words like increased/reduced, or the size of the numbers in "from A to B".
   The direction flips for stats where lower is better (cooldown, cast time, delay, cost, spread,
   recoil, penalty, self-damage, reload time, deploy time, time between charges and similar).
4. **Half damage:** "does/deals half damage" (usually to objectives) is −1.
5. **Additions:** "now also", "now grants/applies/deals/...", "can now", "added" are +1.
6. **Redistributed:** "same overall/total damage" is 0.
7. **"Now only":** a limited drawback ("now only goes on cooldown for 20s", "now only slowed when")
   is +1; "starts on cooldown" is −1; "now has −X% bullet/spirit resist" is −1.
8. **New drawbacks:** "now slows your/you", "now costs/requires/only", "now breaks", "can only",
   "can be dispelled/interrupted/destroyed" are −1.
9. **New behaviour:** "now starts/scales/allows/causes/lets you/has/reflects/refunds/resets/counts/
   triggers/affects", "allows", "again" are +1.
10. Everything else is 0.

Every line counts the same, so a 1% tweak and a big rework weigh equally.
Viewers can override a tag on the page; overrides stay in that browser's localStorage.

## Accuracy checks

All on 2026-11-27, judged by hand. "Debatable" means a player could reasonably argue either way.

| Check | Lines | Right | Debatable | Wrong |
|-------|-------|-------|-----------|-------|
| All "no longer" lines, after the "no longer" rule | 154 | ~149 | ~5 | – |
| Random sample (seed 20261127), rules before this pass | 100 | 83 | 5 | 12 |
| Same sample after fixes (used to tune, so optimistic) | 100 | 95 | 5 | 0 |
| Fresh holdout sample (seed 7331), before its own fixes | 50 | 44 | 1 | 5 |

Best honest estimate: about **88–90% of hero lines are tagged right**, 2–5% are debatable and
about 8–10% are wrong. The holdout sample is the fairest number because no rule was tuned on it
before it was scored. Three of its five misses were fixed afterwards (half damage worded "now
deals", "time between charges", "now causes"). Known leftovers include "Air Drop now lets you
choose to reduce your upward momentum" (tagged nerf, is a buff) and "Assassinate starts at 25%
power instead of 50%" (tagged neutral, is a nerf).

Also fixed in this pass: the "changed from" neutral rule had been saved with backspace characters
instead of `\b`, so it never matched. Upgrade swaps had been scored by comparing unrelated numbers
("+3m Radius" against "+1 Charge"); about 150 such lines are now neutral.

Samples are saved as `data/sample100.json` and `data/sample50_holdout.json` (git-ignored).
For the next check, draw a new sample with a new seed so it hasn't been tuned on.

## Hero numbers

- **Net buffs** = buffs − nerfs over the patches on or after the "Count changes made since" date.
- **Running buff score** = the cumulative net per patch that touched the hero.
- **Win rate** = wins / matches over the last 14 days, all ranks, from
  `api.deadlock-api.com/v1/analytics/hero-stats`. Heroes under 500 matches have no win rate.
- **Pick rate** = hero matches / all hero matches × 12 (12 heroes per match).

## Tiers

Each hero's value is turned into a z-score (distance from the average in standard deviations):

- Win rate mode: z of win rate. Both mode: 0.7 × z(win rate) + 0.3 × z(net buffs).
  Net buffs mode: z of net buffs over the selected range.
- Cut-offs: S ≥ 1.25, A ≥ 0.5, B ≥ −0.1, C ≥ −0.7, D ≥ −1.3, otherwise F.
- Heroes without a win rate are left out of the win-rate and both modes.
