# Decisions

Why things are the way they are. Architecture decisions are presented to the owner first
(options, trade-offs, recommendation) and recorded here once the owner has chosen.
Newest first.

## 2026-11-27: Hand-review every hero line; add win rate around patches, change sizes, rank filter

- **Context:** The owner asked for buff/nerf tags to be "as accurate as possible" and for the three
  proposed upgrades (win rate before/after each patch, change size per line, a better tier list).
- **Options for accuracy:** keep tuning keyword rules (~89% measured) or review every line by hand
  with two independent reviews and a judge for disagreements.
- **Recommended and chosen:** full review (owner asked for subagents and maximum accuracy).
  Results live in `scoring/reviewed_tags.json`; the rules stay as the fallback for new patches.
- **Upgrades chosen by the owner:** all three ("fix all of these"). Change size is shown per line
  rather than folded into a weighted score, because weighting different stats against each other
  would be invented. Win rates are steadied toward the average with a 1,000-match prior.
- **Consequences:** the data build makes about 45 more API calls (rank groups and two windows per
  hero patch); `data.json` grew from ~445 KB to ~520 KB. New patches need a review pass to keep
  every tag hand-checked.

## 2026-11-27: Deploy with GitHub Actions and refresh data daily

- **Context:** The owner granted the `workflow` token scope so deploys and data refresh can run on
  GitHub. Replaces the manual `gh-pages` branch deploy below.
- **Options:**
  1. Refresh in CI and deploy without committing: live data stays fresh, repo history stays small;
     `site/data.json` in the repo goes stale and is only a fallback.
  2. Refresh in CI and commit the new data: repo always matches the site; adds about 450 KB of
     history per day because win rates change daily.
- **Recommended:** option 1, daily at 06:17 UTC, falling back to committed data if an API fails.
- **Chosen by the owner:** automatic deploys and a scheduled refresh (owner enabled the scope for
  this); option 1 picked as the default.
- **Consequences:** the live site can differ from the repo's `data.json`. Revisit if the owner
  wants the data history in git, or a different schedule.

## 2026-11-27: Host on GitHub Pages from a `gh-pages` branch (superseded)

- **Context:** The site needs a public address so search engines can index it. The first preview
  was a private claude.ai artifact, which search engines are unlikely to index.
- **Options:**
  1. GitHub Pages via an Actions workflow: deploys on every push; needs the `workflow` token
     scope, which the current `gh` login lacks.
  2. GitHub Pages from a `gh-pages` branch: works now; deploys are a manual
     `git subtree push --prefix site origin gh-pages`.
  3. Cloudflare Pages: also free; another account and dashboard to manage.
- **Recommended:** option 1, falling back to option 2 until the token has the scope.
- **Chosen by the owner:** GitHub Pages (owner approved). Option 2 is in place because option 1's
  push was refused.
- **Consequences:** deploys are manual. Revisit once `gh auth refresh -s workflow` has been run:
  an Actions workflow could also refresh the data on a schedule.

## 2026-11-27: Name the site Deadlock Patchwatch

- **Context:** The site should rank for "Deadlock" searches, be memorable, and cover more than buffs.
- **Options:** Deadlock Buff Tracker (descriptive, crowded word), Buffed or Nerfed (catchy,
  "Deadlock" only in the title), Deadlock Patchwatch (short brand, covers nerfs, notes and tiers).
- **Recommended:** Deadlock Patchwatch.
- **Chosen by the owner:** Deadlock Patchwatch.
- **Consequences:** browser title is "Deadlock Patchwatch: every hero buff and nerf, patch by patch".

## 2026-11-27: Patch notes from the Steam news API

- **Context:** The official forum changelog and the community wiki both serve bot challenges to
  scripts. No complete public archive was found on GitHub.
- **Options:**
  1. Steam news API: official text, full history of announcements since 2024-10-25, no key.
  2. Forum or wiki: complete history, but blocked for scripts; getting around that is off limits.
- **Recommended:** option 1.
- **Chosen by the owner:** not chosen explicitly; built this way in the first session and kept
  by the owner since.
- **Consequences:** patches before 2024-11-08 and forum-only minor patches are missing
  (see `docs/LIMITATIONS.md`).

## 2026-11-27: Static site with a data snapshot, no backend

- **Context:** A simple, free, fast site; the data changes only when Valve patches.
- **Options:** live fetches from the browser (APIs may block cross-site calls, slower) or a
  pre-built `data.json` refreshed by `build_data.py`.
- **Recommended:** pre-built snapshot.
- **Chosen by the owner:** not chosen explicitly; built this way in the first session.
- **Consequences:** data is as fresh as the last `build_data.py` run and deploy.

## 2026-11-27: One point per line for buffs and nerfs

- **Context:** The owner wants to see how much a hero has been buffed. Change sizes vary wildly
  and aren't comparable across stats.
- **Options:** +1/−1/0 per line (simple, explainable, ignores size) or a weighted score (needs a
  model of each stat's value; easy to get wrong).
- **Recommended:** +1/−1/0 per line, with on-page correction.
- **Chosen by the owner:** not chosen explicitly; the owner has used and corrected it.
- **Consequences:** a big rework and a 1% tweak count the same. See `docs/scoring.md`.
