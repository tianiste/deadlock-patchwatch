# Decisions

Why things are the way they are. Architecture decisions are presented to the owner first
(options, trade-offs, recommendation) and recorded here once the owner has chosen.
Newest first.

## 2026-11-27: Host on GitHub Pages from a `gh-pages` branch

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
