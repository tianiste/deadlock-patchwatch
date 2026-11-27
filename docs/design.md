# Design

The look follows Valve's "City Never Sleeps" update page as broken down in the owner's design
study (`Deadlock_Design_Study.pdf`, captured 2026-11-27): a printed city guide on ink-black paper
with grain, cream type, postcard-framed art, cyan route markers and dashed HUD callouts.
This is a fan site, so it borrows the language, not Valve's logos or title artwork.

## Tokens (top of `site/index.html`)

| Token | Dark (default look) | Light (cream paper) | Use |
|-------|---------------------|---------------------|-----|
| `--ground` | #100E0E ink | #F7E9D5 cream | page background |
| `--sheet` | #1A1716 | #FDF5E8 | tables, panels |
| `--ink` | #F7E9D5 | #100E0E | text |
| `--faded` | #B3A38F | #6B5C4C | secondary text |
| `--rule` | cream at 13% | #E0CCB0 | borders, dashed callouts |
| `--frame` | #F7E9D5 | #FFFAF1 | postcard frames, title fill |
| `--cyan` | #60CDE3 | #1B7D91 | navigation: active tab, sort arrow, route stops, selection |
| `--buff` | #97DA79 | #3B7C25 | buffs only |
| `--nerf` | #E3633C | #C2471F | nerfs only |
| `--hl` | #FFE14D | #FFE14D | search highlight |
| `--sticker` | #E3633C | #E3633C | the "Updated daily" sticker and title shadow |
| tiers | S #E3633C, A #FFE14D, B #97DA79, C #60CDE3, D #B9A68C, F #8C7B8F | | tier letters |

Reference colours from the study: ink #100E0E, cream #F7E9D5, blue #60CDE3, green #97DA79,
yellow #FFE14D, sticker orange ~#E3633C. Light-theme versions are darkened for contrast on cream.

## Type

- Lilita One stands in for Valve's Oracle (not publicly available): title, hero names, patch titles,
  tabs, tier letters, stat numbers.
- Jost for body text (the reference uses Jost too), 17px base.
- Sentence case everywhere.

## Layout

- Masthead: compact black strip with the name and the fan-site note.
- Hero: oversized postcard-lettered title (cream fill, ink outline, orange offset shadow, sizes in
  `em` so it scales), a tilted orange sticker, the intro and range picker, then a strip of tilted
  portrait postcards for the most-buffed heroes in the selected range.
- Sticky bar: tabs with a cyan underline, hero filter, search.
- Heroes: sortable table; hero panel with the portrait in a tilted postcard frame and stats in
  dashed HUD callouts.
- Tier list: tier letter blocks in their own colours, hero postcards tilted alternately.
- Patch notes: a dotted cyan route with numbered stops (patch number in chronological order).
- Grain: a static SVG noise overlay; no texture animation.
- Motion: postcards straighten on hover/focus only, and only without reduced motion.
