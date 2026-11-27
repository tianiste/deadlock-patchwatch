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

1. **Neutral:** fixes, visual, tooltip, sound, animation and model changes; reworks, rescales and
   redistributions; "changed from ... to ...", "is now ...", "now works/uses/scales".
2. **"No longer" lines:** removing a drawback is +1 (reduced damage, penalties, costs, cast
   time, delays, interruptions, self-damage, minimum lifetimes, wake-ups, being disabled), removing a
   benefit is −1 (damage, cooldown cuts, enemy debuffs, unstoppable, death prevention).
   "Can no longer be destroyed/interrupted/dispelled" is +1; any other "can no longer" is −1.
   "Cooldown no longer starts after the ability ends" is +1.
3. **Up or down:** words like increased/reduced, or the size of the numbers in "from A to B".
   The direction flips for stats where lower is better (cooldown, cast time, delay, cost, spread,
   recoil, penalty, self-damage, reload time and similar).
4. **Additions:** "now also", "now grants/applies/deals/...", "can now", "added" are +1.
5. Everything else is 0.

Every line counts the same, so a 1% tweak and a big rework weigh equally.
Viewers can override a tag on the page; overrides stay in that browser's localStorage.

Last accuracy check (2026-11-27): all 154 "no longer" lines were read by hand after the rule
change; about 5 remain debatable (for example "Life Drain is no longer cancellable").
No random sample of the other ~2,400 lines has been scored for accuracy yet.

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
