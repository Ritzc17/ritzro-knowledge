# Male Acolyte — Palette Mapping

Reference: RitzRO palette reverse-engineering guide v0.8.

## Asset information
- SPR version: 2.1
- Indexed frames: 110
- ACT version: 2.5
- ACT actions: 104

## Working index mapping

| Indices | Role |
|---|---|
| 73–79 | Primary |
| 9, 11, 12, 14, 15 | Secondary |
| 56 | Primary / Secondary bridge |
| 13, 49–55 | Tertiary |
| 1–2, 10, 16–23, 25–31, 65–66, 68 | Quaternary |
| 43–48 | Outline / edge |
| 81–89 | Belt / accessory |
| 34, 36–37, 39–40 | Neck / collar shadow — preserve |
| 8, 70–72 | Unresolved — preserve |

## Important discoveries

Index 56 is shared between the Secondary frock and
Primary robe highlights. Strongly contrasting palettes
may require a muted bridge color.

Do not assume that unchanged reference-palette indices
are necessarily protected.

Preserve shading and validate multiple animation frames.

Full documentation: ../../../docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md
