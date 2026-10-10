# RitzRO knowledge transfer for Codex

Prepared 2026-10-10 from accessible ChatGPT Library artifacts and limited accessible conversation context.

## What is complete
- `docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md` — newest saved palette research document; this is the authoritative **starting point**, but verify against actual assets.
- `docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.1.md` through `v0.6.md` — historical versions, preserved unmodified.
- `tools/ro_spr_palette_mapper.py` — actual saved Python mapping utility, preserved unmodified.

## What is NOT complete

## Suggested usage
On the VPS extract into `~/ritzro-knowledge/`, then from the actual project directory ask Codex to inspect `~/ritzro-knowledge/README.md` and the v0.7 documentation. Use explicit file paths, since Codex may not scan outside its current working directory automatically. Before changing live palettes, compare the documentation to current sprite/palette assets and make backups.

## Language/filename note
The correct Korean palette directory may be represented as `몸` or legacy-encoded/mojibake bytes in various tooling. Do **not** assume a Unicode path or copy from one directory to another without inspecting the actual filesystem and client asset lookup. This was a recurring source of deployment confusion.

## Source integrity
Original Library Markdown and Python files were copied byte-for-byte; chat-recovery summaries and this README are newly authored.


## Repository organization

- `classes/` — Class-specific SPR, ACT, reference palettes, releases, and experiments.
- `classes/<job>/male/` — Male character assets and palette research.
- `classes/<job>/female/` — Female character assets, when available.
- `docs/palettes/` — Palette reverse-engineering documentation, versions 0.1–0.8.
- - `experiments/` — Historical diagnostic experiments.
- `tools/` — Sprite and palette analysis utilities.
- `SHA256_MANIFEST.json` — Asset integrity information.

### Current supported classes

Acolyte, Thief, and Hunter currently have male sprite assets.
Female directories are placeholders and must not be assumed to contain validated assets.

### Palette documentation

The primary technical reference is:

`docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md`

Older versions are retained for historical reference.
