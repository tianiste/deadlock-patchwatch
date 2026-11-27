# Known limitations

What the project does not do yet, or does only approximately. Add every new known
limitation when it is found; remove it when it is fixed.

| Limitation | Effect for the user | Why / blocked on | Since |
|------------|---------------------|------------------|-------|
| No patches before 2024-11-08, and minor patches posted only on the forum are missing | A hero's history starts in Nov 2024 and skips some small 2025 hotfixes | Only the Steam news API is fetchable; forum and wiki block scripts | 2026-11-27 |
| Buff/nerf tags are guessed from wording | Some lines are tagged wrong or neutral, especially "changed from X to Y" upgrade swaps | Heuristic rules in `classify()` | 2026-11-27 |
| Every change counts as one point | A 1% tweak and a full rework weigh the same in net buffs | No model of each stat's value | 2026-11-27 |
| Tag corrections are saved only in the viewer's browser | Fixes made on the page don't reach other people or the repo | Static site, no backend | 2026-11-27 |
| Data refreshes once a day | A patch can take up to a day to appear on the site | Daily schedule in the Pages workflow | 2026-11-27 |
| Win rates are all ranks over 14 days | No rank filter; tiers shift as the snapshot ages | Kept simple; fetched once per build | 2026-11-27 |
| Item, map and general changes are not scored | Global changes (for example "all heroes +5% bullet growth") don't affect any hero's score | Only lines naming a hero are scored | 2026-11-27 |
| The claude.ai preview copy is not kept in sync | That link shows an older version | GitHub Pages is now the real site | 2026-11-27 |
