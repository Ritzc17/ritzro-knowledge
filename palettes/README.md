# RitzRO Sprite & Palette Workspace

This directory contains the assets, documentation, and experiments
used to develop custom character sprites and palettes for RitzRO.

## Body (`body/`)

- `classes/<job>/<gender>/` — Job-specific SPR, ACT, and PAL files.
- `docs/` — Body palette reverse-engineering documentation.
- `experiments/` — Earlier palette analysis experiments.
- `archives/` — Historical palette packs and development assets.
- `tools/` — Body-specific utilities, when needed.

All classic jobs through the transcendent second classes are
intended to be supported.

## Hair (`hair/`)

- `styles/male/` — Male hairstyle SPR and ACT assets.
- `styles/female/` — Female hairstyle SPR and ACT assets.
- `colors/original/` — Original client hair-color palettes.
- `colors/custom/` — Custom RitzRO hair-color palettes.
- `docs/` — Hair sprite and palette research.
- `tools/` — Hair-specific utilities, when needed.

Hair-color palettes are maintained separately from hairstyle sprites
because a color may be applicable to multiple hairstyles.

## Shared (`shared/`)

Reserved for utilities and reference material applicable to both
body and hair sprite workflows.

## General utilities

Common scripts currently remain in the repository-level `tools/`
directory, including `ro_spr_palette_mapper.py`.

## Asset extraction

Prefer RitzRO's documented RemoteClient HTTP asset endpoint,
which serves loose overrides or extracts files from client GRFs.

Do not introduce external GRF extraction utilities without approval.

## Preservation

- Preserve original SPR, ACT, and PAL files.
- Record original Korean asset paths and source information.
- Keep original palettes separate from generated palettes.
- Preserve historical experiments and documentation.
- Validate generated PAL files before deployment.
- Do not modify the live client assets without explicit approval.
