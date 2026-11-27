# Design

The look is a 1920s precinct ledger, taken from Deadlock's occult New York: verdigris ground,
brass for emphasis, paper-coloured text. Hero portraits carry the colour; the rest stays quiet.

## Tokens (top of `site/index.html`)

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--ground` | #e4ebe6 | #13201d | page background |
| `--sheet` | #f2f5f1 | #1a2a26 | tables, panels, cards |
| `--ink` | #16241f | #ebe4cf | text |
| `--faded` | #5b6b64 | #93a39b | secondary text |
| `--rule` | #c6d3cb | #2b3d38 | borders |
| `--brass` | #8a6420 | #d1ad62 | accent, selection, links |
| `--buff` / `--nerf` | #12775b / #ad3727 | #6fdcbc / #f0735f | buff and nerf only |
| `--tS` ... `--tF` | | | tier letter colours |

Both themes follow `prefers-color-scheme`, and `data-theme` on the root overrides it.

## Type

- Limelight (art-deco display) only for the site title, the hero name in the panel, patch titles
  and tier letters.
- Barlow Semi Condensed for everything else, with tabular numbers in tables.
- Sentence case everywhere; no all-caps labels and no monospace labels.

## Layout

- Header: title and intro on the left, the "Count changes made since" picker on the right.
- Sticky bar: tabs (Heroes, Tier list, Patch notes), hero filter, search.
- Heroes: sortable table on the left, hero panel on the right (stacks under 920px).
- Tier list: one row per tier, hero portrait cards inside.
- Patch notes: one collapsible block per patch, hero lines start with the hero's icon.
- Green and red mean buff and nerf and nothing else.

## Hero art

Portraits (`*-sm.webp` 128×128, `*-card.webp` 280×380) and each hero's colour come from the
Deadlock API assets. They are game art owned by Valve, used on a fan site.
