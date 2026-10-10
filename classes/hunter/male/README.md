# Male Hunter — Palette Mapping

Reference: RitzRO palette reverse-engineering guide v0.8.

## Asset information
- SPR version: 2.1
- Indexed frames: 124
- ACT version: 2.5
- ACT actions: 104
- Used nontransparent indices: 62

## Working index mapping

| Indices | Role |
|---|---|
| 0 | Reserved / transparency |
| 1 | Dynamic highlight — chest and shoulders |
| 2–7 | Unresolved — preserve |
| 8–15 | Shirt / upper Secondary |
| 16–23 | Tertiary — equipment |
| 24–31 | Lower harness / lower Secondary |
| 32–39 | Protected exposed-arm skin |
| 40 | Unresolved — preserve |
| 41–47 | Quaternary details |
| 48–50 | Unresolved — preserve |
| 51–55 | Tertiary details |
| 56–60 | Upper-body-dominant Primary |
| 61–63 | Lower-body-dominant Primary |
| 64 | Unresolved — preserve |
| 65–71 | Quaternary trim |
| Other indices | Preserve unless analyzed |

## Important discoveries

Indices 8–15 and 24–31 are independently colorable.
Diagnostic red/cyan reversals revealed separate upper
shirt and lower harness regions.

Index 1 controls bright chest/shoulder highlights.
It can be recolored to complement the theme.

Indices 32–39 contain exposed arm skin and must remain
unchanged when generating clothing palettes.

Indices 56–63 are shared between upper and lower body.
The 56–60 and 61–63 split is provisional, not a
perfect jacket/pants separation.

## Palette design

Design families established during Hunter experiments:

- 1–10: Strong primary colors
- 11–20: Realistic ranger and fieldwear colors
- 21–30: Experimental fluorescent colors
- 31–40: Wildcards and unusual combinations

Allow complementary, analogous, monochromatic,
warm/warm, and cool/cool combinations.

Do not enforce one color relationship across all
40 palettes. Preserve readable shading.

## Historical release notes

Original v7 palettes: releases/v7/

Revisions of palettes 1–2:
experiments/revised_01_02/

The installed selection previously used the Bright
Pants revision for slots 1–2 and v7 for slots 3–40.
Verify current deployment before treating this as live.

## Deployment

Do not install without user approval of the preview.

Production palette overrides require CP949-to-Windows-1252
mojibake for every Korean path component.

See the main v0.8 guide for deployment procedures.

Full documentation: ../../../docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md
