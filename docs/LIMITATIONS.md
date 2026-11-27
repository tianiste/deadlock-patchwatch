# Known limitations

What the project does not do yet, or does only approximately. Add every new known
limitation when it is found; remove it when it is fixed.

| Limitation | Effect for the user | Why / blocked on | Since |
|------------|---------------------|------------------|-------|
| No patches before 2024-11-08, and minor patches posted only on the forum are missing | A hero's history starts in Nov 2024 and skips some small 2025 hotfixes | Only the Steam news API is fetchable; forum and wiki block scripts | 2026-11-27 |
| Lines from patches after 2026-11-26 are tagged automatically until reviewed | New lines can be wrong about 1 time in 10 until someone reviews them (dashed tags) | Reviews are run by hand per patch; see `docs/scoring.md` | 2026-11-27 |
| About 570 hero lines are tagged neutral, some because the effect is genuinely unclear | Those changes don't move a hero's net score | Reviewers chose 0 over guessing | 2026-11-27 |
| Every change counts as one point | A 1% tweak and a full rework weigh the same in net buffs | No model of each stat's value | 2026-11-27 |
| Tag corrections are saved only in the viewer's browser | Fixes made on the page don't reach other people or the repo | Static site, no backend | 2026-11-27 |
| Data refreshes once a day | A patch can take up to a day to appear on the site | Daily schedule in the Pages workflow | 2026-11-27 |
| Win rates cover 14 days, in three rank groups only | No per-rank view for lower ranks; tiers shift as the snapshot ages | Kept to three API calls per build | 2026-11-27 |
| Win rate before/after a patch is all ranks and up to 7 days each side | Other patches, items and meta also move win rates, so a shift isn't proof the patch caused it | Patches are often close together | 2026-11-27 |
| Change sizes only appear on lines with one clean number pair | About 55% of lines (swaps, multi-stat lines) show no % | Comparing different stats would be invented math | 2026-11-27 |
| Item, map and general changes are not scored | Global changes (for example "all heroes +5% bullet growth") don't affect any hero's score | Only lines naming a hero are scored | 2026-11-27 |
| The claude.ai preview copy is not kept in sync | That link shows an older version | GitHub Pages is now the real site | 2026-11-27 |
