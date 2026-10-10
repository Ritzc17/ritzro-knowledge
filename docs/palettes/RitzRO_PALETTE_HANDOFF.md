# RitzRO palette research — Codex handoff

## Scope and provenance
This is a structured handoff of the long ChatGPT RitzRO palette-editing conversation, **not a verbatim transcript**. It summarizes user observations, generated revisions, confirmed binary findings and working hypotheses. See the bundled v0.1–v0.4 research notes, SPR/ACT/PAL source files, mapper, and v1–v5/v1–v3 ZIP archives. Preserve uncertainty: not every visually inferred semantic mapping has been conclusively established.

## Infrastructure and installation
- VPS user: `debian`; project: `/home/debian/ritzro-client/RitzRO`.
- rAthena checkout: `~/rathena`; roBrowserLegacy RemoteClient service: `ritzro-remoteclient`.
- Client loose overrides: `/home/debian/ritzro-client/RitzRO/data/palette/`.
- Korean original `몸` (body) may be requested through CP949-decoded mojibake path `¸ö` by the RemoteClient. Acolyte male filename previously used `¼ºÁ÷ÀÚ_³²_<ID>.pal`; Thief male `µµµÏ_³²_<ID>.pal`. **Verify actual current path and encoding before writing.**
- Cache refresh previously used: `rm -rf ~/roBrowserLegacy-RemoteClient-Rust/data && sudo systemctl restart ritzro-remoteclient`.
- To copy terminal output into Windows clipboard via OSC52, use `2>&1 | tee >(clip52)` when output is requested.
- Build only the online roBrowser client with `npm run build:online` when necessary.
- Stylist supports clothing IDs 1–15 in the working setup; 11–15 were diagnostics. Do not overwrite other job classes or change server maximum without checking config.

## Palette file format and tools
- `.pal`: 1024 bytes = 256 entries × 4 bytes; RGB are first three bytes; preserve the fourth byte.
- `.spr`: indexed pixels store palette indices. `.act`: frame/layer/direction references. Binary pixel masks are superior to manual in-game contact sheets for mapping indices.
- Reusable `ro_spr_palette_mapper.py` is bundled inside `ro_spr_palette_mapper_and_thief_report.zip`, along with an HTML report, CSV, and exact masks. Extract it and use with Python + Pillow.
- Main lesson: index groups are sprite-specific and can be noncontiguous; one index can serve two different garment regions.

## Male Acolyte research and current production v5
Source: `acolyte_male.spr`, `.act`, and `_692.pal`. See `RitzRO_PAL_Reverse_Engineering_v0.4.md` for extensive methodology, diagnostic history, and mappings.

Current working map:
- Primary main robe: `73–79`.
- Secondary shoulder frock: `9,11,12,14,15`.
- Shared Primary/Secondary highlight: `56` — large frock patch **and** sparse robe highlight pixels. Must coordinate hue and brightness; dark bridge creates ugly brown shadows when primary and secondary hues are similar (notably style 10 red/crimson). For similar hues use a brighter coordinated highlight; for highly contrasting hues use a moderated bridge.
- Tertiary cuffs/glove shadow and garment details: `13,49–55`.
- Quaternary leather/shoes: `1–2,10,16–23,25–31,65,66,68`.
- Outline/edge: `43–48`, keep dark/muted.
- Belt accessory: `81–89`, often Secondary-derived.
- Neck shadow `34,36,37,39,40`: preserve; unresolved `8,70–72`: preserve.
- Latest generated Acolyte production: `ritzro_acolyte_v5_1_10.zip`.

## Ten design themes (P / S / T / Q)
1. Black / Crimson / Crimson red / Oxblood leather
2. Black / Navy / Medium royal blue / Blue-black leather
3. Emerald / Brown / Warm lighter brown / Warm brown leather
4. Sky blue / Cloud white / Pale blue / Tan leather
5. Cream / Black / Warm taupe-brown / Dark brown leather
6. Black / Charcoal / Gold / Antique-gold leather
7. Orange / Blue / Lighter blue / Dark brown leather
8. Purple / Black / White / Charcoal-violet
9. Charcoal / Dark charcoal / Medium charcoal / Near-black leather
10. Red / Crimson / Gold / Dark chestnut

Hex anchor values from v4/v5 are in the bundled README files; use those exact values for continuity. For Acolyte, style 1 and 2 use `#151619` Primary; Thief v3 lightened their Primary to `#2A2D32` and `#2B2F36` to preserve pants texture.

## Male Thief research
Source `thief_male.spr`, `.act`, `_0.pal`–`_4.pal`. SPR 2.1, 116 indexed frames, 64 used nontransparent indices. Palette IDs 0–3 have large black gaps at used indices; ID 4 is first good base and MUST be used for custom generation. The initial corrupted palettes were not merely a rendering glitch.

Thief v3 working map:
- Primary pants `16–23`.
- Secondary jacket `9,10,57–63,72–79`. Indices 9/10 were changed to Secondary highlights in v3 to fix cream jacket splotches. 9 is shared/more widely reused; 10 is more jacket-specific.
- Tertiary gloves/main shoes `24–39`.
- Quaternary rear boot panels `64–71`.
- Accessory undershirt `40–47` (light coordinated hue).
- Kneepads `48–55` (contrasting leather-derived hue).
- `72–79` also affects boot tips, so matching jacket and shoe colors is a compromise.
- Latest generated Thief production: `ritzro_thief_v3_1_10.zip`.

### Latest user observations and unresolved issue (STOPPING POINT)
- Thief v3 improved jacket coloration and black-pants detail in styles 1–2.
- **Still present:** an obvious white/light patch on the chest undershirt, plus scattered white speckles on jacket and belt/waist. The user wants these exact indices identified **programmatically from the decoded SPR pixel data**, not by inspecting generated mask images repeatedly.
- Need to distinguish true undershirt indices from a **shared undershirt/jacket/belt highlight index**. Do not claim an index without evidence from frame pixel coordinates, counts, neighborhood/connected-component analysis, and matching palette RGBs.
- Thief style 6 (black pants, charcoal jacket, gold gloves/boots) has best visual separation. For Thief, jacket and gloves touch and require meaningful hue/luminance contrast; schemes with similar Secondary and Tertiary tend to merge visually.
- Next: (1) query exact Thief `.spr` indices for pale chest/shoulder/belt pixels, using frame coordinates/connected regions and source palette RGB; (2) report findings and confidence; (3) only then produce Thief v4 1–10, maintaining style 6 contrast as a design lesson.
- Existing `ro_spr_palette_mapper.py` can decode indexed frames; extend it for coordinate-based semantic analysis rather than guessing from montages. ACT may be needed for exact animation/direction frame mapping.

## Testing and deployment workflow
1. Generate PAL files using known-good class-specific base.
2. Place numbered `.pal` in loose override directory under exact expected encoding/path; do not overwrite other class files.
3. Clear RemoteClient cache and restart `ritzro-remoteclient` (rAthena restart not normally needed for replacing existing palette IDs).
4. Test front, side, back in stylist; user has been providing contact sheets.
5. Record confirmed findings in new versioned Markdown notes, preserving older revisions.

## Export limitations
This package includes available artifacts and this structured handoff, but **not the complete verbatim ChatGPT conversation or every user screenshot**. For full transcript, use ChatGPT's conversation/account export separately and copy that archive to the VPS.
