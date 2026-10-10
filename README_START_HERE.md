# RitzRO Palette Work — Codex Handoff (2026-10-10)

## Scope and provenance
This is a **technical handoff summarizing the conversation**, not a verbatim ChatGPT transcript. It includes the v0.7 generalized guide, historical documentation, latest available generated palette archives, and uploaded male Thief source assets. Screenshots and earlier chat messages are not all included; use the ChatGPT export for a verbatim archive. Do not assume this handoff covers unrelated RitzRO project conversations.

## Current deliverables
- `palettes/ritzro_thief_v4_1_40.zip`: latest male Thief 40-palette revision.
- `palettes/ritzro_acolyte_v3_1_40.zip`: latest male Acolyte 40-palette revision; #40 black/hot pink preserved from earlier version.
- `classes/thief/male/reference/thief_male_copy.spr`, `.act`, `classes/thief/male/reference/thief_male_0.pal`: uploaded Thief reference assets.
- `docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md`: main procedural and mapping reference. Earlier revisions for audit trail.

## Core procedure
Parse the exact SPR indexed frames; inspect pixel index counts, coordinates, components, body zones and ACT action/direction references. Use diagnostic renders and human visual judgment to label garment families. Store mappings by exact sprite hash. Never assume class/sex variants share indices. Preserve unedited PAL bytes and fourth bytes; validated PALs have 256 four-byte entries (1024 bytes).

## Thief working mapping (male only)
- 16–23 pants Primary; 41 extreme pants waistband highlight.
- 9,10 and 57–63 jacket highlight; 75–79 jacket main Secondary.
- 24–31 equipment component A; 32–39 component B. BOTH affect gloves AND boots, yielding intentional two-tone equipment; they do not separate glove color from boot color.
- 72–74 footwear details (not jacket); 73 produces large toe/boot patch; 64–71 rear boot panels.
- 40 undershirt/chest + sparse jacket highlight shared index: jacket-tinted bridge; 42–47 remaining light undershirt/detail indices.
- 48–55 kneepad/accessory details.
- 9 also reaches a few toe pixels: retain vivid jacket color, tolerate minor reuse; do not force compromise.
- Keep distinct glove/pants/jacket value structures and material identity. A nominal black still needs readable charcoal highlights. Brown equipment is not mandatory.

## Acolyte working mapping (male only)
- 73–79 Primary robe; 9,11,12,14,15 Secondary frock; 56 shared frock/robe.
- 13 and 49–55 Tertiary cuffs/trousers; 1–2,10,16–23,25–31,65,66,68 Quaternary gloves/shoes; 43–48 outline; 81–89 belt accessory; 34,36,37,39,40 neck/collar preserve; 8,70–72 unresolved/preserve.
- Index 56 is crucial: select color to maintain frock internal shading AND plausible Primary highlights. Bright Secondary usually needs dark 56 shadow; dark Secondary may use lighter 56. Style 22 dark purple 56 on pink frock was a success; style 25 bright orange 56 on black robe failed; style 7 bright blue 56 flattened blue frock texture and was corrected to deep blue. Do not use a universal bridge formula.
- Reference-quality styles: Acolyte #4 sky-blue/ivory/tan; #40 black/hot pink. Realistic 11–20 were well received. Fluorescent 21–30 redesigned to color the Primary robe too.

## Iteration history / lessons
Thief began with 10 palettes, expanded to 30 and 40. V4 of the 40-set is latest: #1 vivid scarlet, #2 richer cobalt, #4 sky blue/cloud white, #6 restored black/gold, #40 black/hot pink; 11–20 muted but equipment-varied; 21–30 fluorescent; 31–39 wildcards. Earlier variants muted the colors too much. Acolyte 40-set reached v3; gloves and boots need not be brown, and fluorescent robes should genuinely fluoresce.

## Deployment (PowerShell on Windows, then Bash on VPS)
Extract the chosen archive into `$HOME\Downloads\<archive_stem>`; `scp` the contained `*.pal` to `debian@15.204.86.96:/home/debian/ritzro-client/RitzRO/data/palette/몸/`.
For Thief from the palette directory `/home/debian/ritzro-client/RitzRO/data/palette`:
`for id in {1..40}; do mv "몸/thief_male_${id}.pal" "¸ö/µµµÏ_³²_${id}.pal"; done`
For Acolyte:
`for id in {1..40}; do mv "몸/acolyte_male_${id}.pal" "¸ö/¼ºÁ÷ÀÚ_³²_${id}.pal"; done`
Refresh remote client: `rm -rf ~/roBrowserLegacy-RemoteClient-Rust/data && sudo systemctl restart ritzro-remoteclient`.
rAthena config `~/rAthena/conf/battle/client.conf` should have `max_cloth_color: 40`; after changing, restart with `./athena-start stop` then `./athena-start start` from `~/rAthena`.

## Important limitations
These are working interpretations of tested sprite assets, not universal RO mappings. The original conversation includes visual comparisons and proposed edits, not every proposed edit was shipped. Use actual binaries and visual validation rather than trusting descriptive claims alone.
