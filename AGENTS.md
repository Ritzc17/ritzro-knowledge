# Instructions for Codex working with RitzRO knowledge

- Read `README.md` then `docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md` before palette work.
- Treat the old documentation as research observations with confidence labels, not unconditionally correct universal index maps.
- Each job/sex sprite can use different palette indices; inspect its `.spr` and `.act` before recoloring.
- Preserve all `.pal` bytes other than explicitly targeted RGB values, especially the fourth byte in each 4-byte entry; validate 1024-byte output.
- Do not overwrite working/live palettes without backing up originals and seeking user approval.
- Distinguish sprite-index mapping, visual observations, and inferred semantic labels; test shared indices and multiple actions/directions.
- Inspect the real palette folder encoding before installing assets; check cache and server/client restart requirements.
- For roBrowserLegacy changes build only the online client via `npm run build:online` when necessary. For rAthena startup use `./athena-start start`, not individual server processes.


## RitzRO palette development rules

1. Read `docs/palettes/RitzRO_PAL_Reverse_Engineering_v0.8.md` before generating palettes.
2. Use the exact target class and sex's SPR, ACT, and known-good PAL assets.
3. Never assume palette indices are interchangeable between jobs or sexes.
4. Protect confirmed skin indices and preserve unknown indices.
5. Preserve the fourth byte of every PAL entry unless independently validated.
6. Generate numbered preview sheets for user review.
7. Do not provide production installation instructions until the user explicitly approves the preview.
8. Preserve historical palette revisions and reference assets.

### Mandatory mojibake deployment rule

All Korean directory names and filenames MUST be converted from
CP949 to their Windows-1252 mojibake representation when installing
assets into the live RitzRO RemoteClient data override directory.

This applies to every class, not just Hunter.

Production palette directory:

`/home/debian/ritzro-client/RitzRO/data/palette/`

The directory is `palette`, singular.

Use the exact asset path requested by RemoteClient when validating
production filenames.

The relevant service is `ritzro-remoteclient`.

### Repository navigation

Class assets: `classes/<job>/<sex>/`

Technical documentation: `docs/palettes/`

Palette tools: `tools/`

Do not assume the old root-level sprite paths are still valid.
