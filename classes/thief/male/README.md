# Male Thief — Palette Mapping

Reference: RitzRO palette reverse-engineering guide v0.8.

## Asset information
- Indexed SPR frames: 116

## Working index mapping

| Indices | Role |
|---|---|
| 16–23 | Primary — pants |
| 41 | Primary — waistband highlight |
| 9–10, 57–63 | Secondary — jacket highlights |
| 75–79 | Secondary — jacket main |
| 24–31 | Equipment color component A |
| 32–39 | Equipment color component B |
| 72–74 | Footwear details |
| 40 | Shared undershirt / jacket bridge |
| 42–47 | Undershirt / light details |
| 48–55 | Kneepad / accessories |
| 64–71 | Rear boot panels |

## Important discoveries

Indices 24–31 and 32–39 affect both gloves and boots.
They support two-tone equipment, not necessarily
independent glove and boot colors.

Index 9 is primarily a jacket highlight but also
appears in a few footwear pixels. Minor reuse can be
acceptable when the dominant region looks correct.

Index 40 is shared between the undershirt and jacket,
so a bridge color may be necessary.

Keep gloves, pants, boots, and jacket visually distinct,
and retain readable gradients in dark palettes.

Full documentation: ../../../docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md
