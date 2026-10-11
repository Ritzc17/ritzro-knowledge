# Ragnarok Online `.pal` Reverse-Engineering Notes

**Version:** 0.4  
**Project context:** RitzRO / roBrowserLegacy / 2025 kRO client assets  
**Primary test sprite:** Male Acolyte (`성직자_남.spr`)  
**Status:** Experimental documentation. Binary findings, controlled visual diagnostics, and inferences are labeled separately.

## 1. Purpose

This document records reverse-engineering results for Ragnarok Online character `.pal` files and their relationship to indexed `.spr` sprites and `.act` animation files.

The immediate goal is to support an agent or developer creating a small set of deliberate, high-quality custom clothing palettes without corrupting skin, mounts, accessories, or unrelated sprite regions.

The detailed semantic mappings in this document apply specifically to the tested **male Acolyte body sprite** unless explicitly stated otherwise.

A central conclusion is that semantic labels such as **Primary**, **Secondary**, **Tertiary**, and **Quaternary** must be treated as **sprite/class-specific mappings**, not universal Ragnarok palette addresses.

---

## 2. Rendering model

```text
ACT action/direction
    ↓
ACT animation frame/layer
    ↓
SPR frame number
    ↓
indexed SPR pixel (palette index 0–255)
    ↓
PAL entry
    ↓
displayed color
```

A palette entry is not inherently a semantic object such as "shoe", "robe", or "glove". The same palette index may be reused across disconnected sprite regions.

Therefore maintain two separate concepts:

1. **Palette/index semantics** — e.g. "male Acolyte Secondary color family".
2. **Observed sprite usage** — e.g. "appears on shoulder frock, shoe tips, belt, etc."

---

## 3. `.pal` file structure

### CONFIRMED — binary / controlled editing

Every tested standalone `.pal` file is:

```text
1024 bytes
```

Working structure:

```text
256 entries × 4 bytes = 1024 bytes
```

Offsets:

```text
entry 0   → bytes 0–3
entry 1   → bytes 4–7
...
entry 255 → bytes 1020–1023
```

Editing the first three bytes changes visible RGB color. The fourth byte has been preserved in every diagnostic/custom edit so far.

**Agent rule:** modify RGB bytes only unless the fourth byte is separately verified.

---

## 4. Reference SPR/ACT assets

Reference body sprite:

```text
data\sprite\인간족\몸통\남\성직자_남.spr
```

Reference ACT:

```text
data\sprite\인간족\몸통\남\성직자_남.act
```

Parsed properties:

- SPR version: **2.1**
- Indexed SPR frames: **110**
- Truecolor frames: **0**
- ACT version: **2.5**
- ACT actions: **104**
- ACT references all 110 indexed SPR frames.
- Action structure is 13 animation groups × 8 directions.
- Direction order:

```text
S, SW, W, NW, N, NE, E, SE
```

---

## 5. Actual palette-index usage in male Acolyte SPR

Parsing all 110 indexed frames shows only **66 nontransparent indices** are referenced:

```text
1–2
8–23
25–31
34
36–37
39–40
43–56
65–66
68
70–79
81–89
```

Any other index cannot affect this specific body SPR.

### Important methodological rule

A `.pal` file may contain colors at indices the sprite never references. Comparing palette files alone is not enough. Always consult SPR usage before concluding an entry matters.

---

## 6. Initial multi-palette comparison

Nine known-good male Acolyte palettes from `2025Palettes.grf` were compared:

```text
34
100
105
107
228
251
257
692
699
```

Only these 79 entries varied across the nine files:

```text
1–15
40–55
72–79
88–95
112–127
168–175
192–199
```

### Important correction

In earlier work, entries that did not vary across the sampled palette pack were informally treated as likely "protected".

That is too strong.

The correct conclusion is only:

> These entries were **invariant across the sampled palette pack**.

An invariant entry may still be clothing and may still need recoloring. Index `56` is the key example: it did not vary in the sampled pack, but visual diagnostics show it participates in the Acolyte's Secondary frock region.

Use:

```text
INVARIANT IN SAMPLE SET
```

not:

```text
PROTECTED
```

unless protection has been independently established.

---

## 7. Diagnostics 700–706 — broad candidate blocks

Palette 692 was used as the base.

| Test | Entries | Forced color | Binary usage | Visual result |
|---|---:|---|---|---|
| 700 | `1–15` | Magenta | `1,2,8–15` | Strong visible effect |
| 701 | `40–55` | Green | `40,43–55` | Strong visible effect |
| 702 | `72–79` | Cyan | all 8 | Very strong visible effect |
| 703 | `88–95` | Yellow | only `88–89` | Small/subtle |
| 704 | `112–127` | Red | none | No legitimate effect |
| 705 | `168–175` | Blue | none | No effect |
| 706 | `192–199` | Orange | none | No effect |

### Binary-over-visual correction

An earlier visual impression suggested 704 may have caused a small change. Binary analysis disproved this because indices `112–127` are absent from the SPR.

**Agent rule:** binary SPR usage overrides subjective screenshot inference about whether an index is used.

---

## 8. Diagnostics 707–709 — core color families

### 707 — indices `9–15`

Observed across:

- shoulder/frock details
- glove/hand-area clothing
- shoe-tip accents
- other distributed Secondary pixels

Current classification:

```text
9–15 = Secondary color family
```

The index order appears broadly consistent with a light→dark ramp.

---

### 708 — indices `45–55`

Observed around:

- cuffs
- waist / front-center details
- pants
- lower hem
- footwear/detail pixels

This range is not semantically uniform.

Later diagnostics resolve it as:

```text
43–48 = Outline / edge family
49–55 = Tertiary family
56     = Secondary highlight
```

---

### 709 — indices `73–79`

This clearly recolors the dominant visible garment area in front and rear views.

Current mapping:

```text
73 → brightest highlight
74 → highlight
75 → light
76 → midtone
77 → shadow
78 → deep shadow
79 → darkest shade
```

Current classification:

```text
73–79 = male Acolyte Primary cloth ramp
```

### Usage counts

| Index | Pixels | Frames |
|---:|---:|---:|
| 72 | 125 | 26 |
| 73 | 1,917 | 68 |
| 74 | 10,513 | 110 |
| 75 | 18,614 | 110 |
| 76 | 20,905 | 110 |
| 77 | 7,304 | 110 |
| 78 | 3,791 | 108 |
| 79 | 5,535 | 110 |

`74–79` are workhorse clothing entries. `72–73` are much more specialized.

---

## 9. Production palette prototypes v1–v3

### v1

Generated using:

```text
Primary:   73–79
Secondary: 9–15
Tertiary:  49–55
```

Result:

- main custom colors worked
- persistent cream/off-white front chest / rear frock patch remained

### v2

Tested the hypothesis:

```text
Secondary = 8–15
Primary   = 72–79
```

Diagnostics disproved this:

- index `8` is a specialized shoe/toe detail
- index `72` was not visible in tested idle directions

### v3

Assigned index `56` as a Primary highlight.

This successfully recolored the stubborn cream patch, but the hue was wrong for palettes where Primary and Secondary differed.

Example:

- Palette 7 = Orange Primary / Blue Secondary
- index `56` became light orange
- the affected frock region was otherwise blue

This established that index `56` belongs to **Secondary**, not Primary.

---

## 10. Confirmed male Acolyte semantic mapping

### Primary

```text
73–79
```

Observed role:

- overall majority of robe color
- dominant base garment color

### Secondary

```text
9,11,12,14,15
```

Observed role:

- vest-like frock over the shoulders
- front and rear frock region
- selected shoe-tip/frock details

Later diagnostics moved index `10` to Quaternary and index `13` to Tertiary.

### Primary/Secondary bridge — index 56

```text
56
```

Index `56` is **shared semantically** between two visible regions:

- a substantial portion/highlight region of the Secondary frock
- sparse highlight pixels embedded in the Primary robe

Therefore `56` cannot be assigned perfectly to Primary or Secondary when those hues strongly contrast.

Recommended treatment:

- when Primary and Secondary are close in hue, bias `56` toward a Secondary highlight so it blends naturally with both;
- when Primary and Secondary strongly contrast, calculate a darker, muted, desaturated bridge between the two;
- avoid making `56` brighter or more saturated than both families, because shared pixels then appear as obvious color contamination.

This is a confirmed example of one palette index being shared by two otherwise distinct semantic color families.

### Tertiary

```text
13
49–55
```

Observed role:

- cuffs
- pants
- belt-adjacent accents
- other smaller garment accents
- index `13` acts as a dark Tertiary cuff/glove shadow

### Quaternary

Main and supplemental leather/detail family:

```text
1–2
10
16–23
25–31
65,66,68
```

Observed role:

- gloves
- shoes
- shoe edging / highlights
- front-center zipper/trim
- rear leather/brown details

Interpretation by subgroup:

```text
1–2       glove/shoe outline or edge highlights
10        shoe highlight
16–23     main Quaternary leather/detail ramp
25–31     sparse Quaternary supplemental/glove highlights
65,66,68  shoe highlights
```

These are semantically grouped even though they are numerically noncontiguous.

---

## 11. Functional / derived groups

### Outline / Edge family

```text
43–48
```

Observed role:

- clothing structural outlines
- edge definition
- general silhouette/detail boundaries

Recommended treatment:

- keep dark or muted
- derive from the overall scheme
- preserve strong contrast against the environment and neighboring garment colors

Do **not** make this family bright merely because a scheme is bright.

### Accessory: Belt

```text
81–89
```

Observed role:

- Acolyte belt

Recommended treatment:

- coordinate with Secondary by default
- treat as an accessory family, not part of the core Secondary ramp
- can be independently overridden if a palette design calls for it

### Neck / Collar shadow region

```text
34,36,37,39,40
```

Observed role:

- tiny collar / neck-adjacent shadow pixels

Recommended treatment:

- preserve from the known-good base palette for now
- note as neck/collar shadow region
- avoid recoloring casually because it sits near skin/hair boundaries

### Specialized / unresolved

```text
8
70–72
```

Current status:

- `8` = specialized shoe/toe detail
- `70–72` = not visibly useful in the tested male Acolyte idle directions; preserve for now

---

## 12. Diagnostic 13 — family locator summary

Diagnostic 13 used:

```text
1–2              YELLOW
34,36,37,39,40   CYAN
43–48            RED
65,66,68         ORANGE
70–72            VIOLET
81–89            BLUE
```

Observed interpretation:

```text
YELLOW  → glove/shoe edging, Quaternary-related
CYAN    → tiny collar/neck region
RED     → general structural outlines/edges
ORANGE  → shoe highlights, Quaternary-related
VIOLET  → not visibly important in tested idle directions
BLUE    → belt accessory
```

This diagnostic is a major basis for the v0.3 mapping.

---

## 13. Diagnostic 15 — `43–56` map

Diagnostic 15 individually recolored `43–56`.

Key findings:

```text
43–48 → outline / structural edge family
49–55 → Tertiary garment family
56    → Secondary highlight
```

This establishes a semantic boundary between `55` and `56` despite numerical adjacency.

---

## 14. Updated Acolyte generation model

For the **male Acolyte sprite**, generate custom palettes using:

```text
PRIMARY
73–79

SECONDARY
9–15
56 = extra-light Secondary highlight

TERTIARY
49–55

QUATERNARY
1–2
16–23
25–31
65,66,68

OUTLINE / EDGE
43–48
dark/muted derivative of overall scheme

BELT ACCESSORY
81–89
normally derived from Secondary

NECK/COLLAR SHADOW
34,36,37,39,40
preserve from base for now

SPECIALIZED / UNRESOLVED
8
70–72
preserve from base for now
```

---

## 15. Design-family terminology

Use semantic color-family names instead of garment-only labels:

```text
Primary
Secondary
Tertiary
Quaternary
Outline / Edge
Accessory
Protected / Fixed only when independently established
```

These are **not universal index ranges**.

Correct documentation style:

```text
Male Acolyte:
    Primary   = 73–79
    Secondary = 9–15 + 56
    Tertiary  = 49–55
    Quaternary = 1–2 + 16–23 + 25–31 + 65,66,68
```

Another class may use completely different indices.

---

## 16. Class-specific mapping rule

Open-source Ragnarok sprite/palette tools support a sprite-specific workflow rather than a universal hardcoded color map.

Relevant projects reviewed:

- `ragassets`
- ActEditor
- actOR / Ragnarok.Tools
- RagLite / RagnarokResearchLab
- RagnarokFileFormats

The practical lesson is:

> **Palette-index semantics belong to the specific SPR, not to Ragnarok globally.**

Maintain mappings per body sprite/class/sex/variant.

Recommended future structure:

```text
Male Acolyte
Female Acolyte
Male Swordsman
Female Swordsman
Male Knight
Male Peco Knight
...
```

Only promote a mapping to a global rule after it has been demonstrated across multiple independent sprites.

---

## 17. ACT-aware findings

ACT analysis explains why a palette index may be real yet absent from a small idle screenshot sample.

Example:

```text
index 88
→ appears in only one SPR frame (frame 79)
→ referenced by Frozen/Stun actions
→ relevant to W, NW, N, NE orientations
```

Thus:

- SPR parsing determines whether an index exists.
- ACT parsing determines when/direction where it appears.
- Visual diagnostics assign semantic meaning.

---

## 18. Rules for custom palette generation

For the male Acolyte sprite:

1. Start from a known-good modern palette.
2. Preserve every byte except deliberately targeted RGB values.
3. Preserve the fourth byte of each palette entry.
4. Parse SPR usage before editing indices.
5. Treat Primary/Secondary/Tertiary/Quaternary as sprite-specific semantic families.
6. Do not assume a semantic family is contiguous.
7. Use `73–79` as the Primary ramp.
8. Use `9–15` as the main Secondary ramp and derive index `56` from the brightest Secondary shade.
9. Use `49–55` as the Tertiary ramp.
10. Derive all Quaternary subgroups from one coordinated Quaternary base color.
11. Keep `43–48` dark/muted as the Outline / Edge family.
12. Derive `81–89` from Secondary by default as the belt accessory family.
13. Preserve neck/collar shadow indices `34,36,37,39,40` until there is a reason to change them.
14. Preserve unresolved/specialized indices such as `8` and `70–72` unless specifically mapped.
15. Do not equate "unchanged across sample palettes" with "protected".
16. Validate production palettes with at least an eight-direction contact sheet.
17. For rare/action-specific indices, use ACT-aware rendering or testing.

---

## 19. Recommended v4 palette generator behavior

Given four design colors:

```text
Primary
Secondary
Tertiary
Quaternary
```

derive:

```text
Primary ramp      → 73–79
Secondary ramp    → 9–15
Secondary highlight → 56
Tertiary ramp     → 49–55

Quaternary:
    16–23 main ramp
    25–31 sparse/highlight variant
    1–2 edge/highlight derivative
    65,66,68 shoe-highlight derivative

Outline / Edge:
    43–48 dark muted derivative

Belt accessory:
    81–89 Secondary-derived accessory ramp
```

This is the current recommended production model for **male Acolyte only**.

---

## 20. Generalization strategy for other jobs

For each target body sprite:

1. Obtain `.spr`.
2. Parse every indexed frame.
3. Enumerate used palette indices and pixel counts.
4. Obtain matching `.act`.
5. Map SPR frames to actions/directions.
6. Compare several known-good palettes for that exact sprite.
7. Generate targeted diagnostic palettes.
8. Assign sprite-specific semantic families.
9. Create contact sheets for semantic validation.
10. Document mappings under that exact class/sex/body variant.

For mounted classes, analyze mounted and unmounted body sprites separately.

---

## 21. Confidence terminology

### CONFIRMED — binary

Established from parsed file data.

Example:

> Male Acolyte SPR does not reference indices `112–127`.

### CONFIRMED — visual diagnostic

Established through a known-color test.

Examples:

> `73–79` is the male Acolyte Primary robe family.

> Index `56` is part of the Secondary frock and functions as a bright highlight.

> `43–48` is an Outline / Edge family.

### INFERRED

Strongly suggested but not uniquely proven.

Example:

> Belt `81–89` should normally inherit Secondary hue.

### UNKNOWN / PRESERVE

Not yet established strongly enough to recolor safely.

Current examples:

```text
8
70–72
```

---

## 22. Current male Acolyte working map

```text
PRIMARY
73–79
→ majority of robe

SECONDARY
9–15
56
→ shoulder frock / vest-like area
→ shoe tips
→ 56 is bright highlight

TERTIARY
49–55
→ cuffs
→ pants
→ belt-adjacent accents

QUATERNARY
1–2
16–23
25–31
65,66,68
→ gloves
→ shoes
→ zipper / front center trim
→ shoe edging/highlights
→ rear leather details

OUTLINE / EDGE
43–48
→ garment edge definition
→ keep dark/muted

ACCESSORY: BELT
81–89
→ belt
→ usually coordinate with Secondary

NECK/COLLAR SHADOW
34,36,37,39,40
→ preserve for now

SPECIALIZED / UNRESOLVED
8
70–72
→ preserve for now
```

---

## 23. Core methodology

> **Parse first, recolor second, visually label third.**

Binary SPR/ACT analysis establishes what can be affected and when it appears. Controlled diagnostics establish what those used indices mean visually. Production palette generation comes only after those two steps.


---

## 24. v5 refinements and shared-index rule

Further diagnostics after v0.3 refined the male Acolyte generator.

### Index 10

Observed as a shoe-only highlight rather than part of the frock.

```text
10 → Quaternary shoe highlight
```

### Index 13

Observed around cuffs/glove areas and reassigned as a dark Tertiary shadow.

```text
13 → Tertiary dark cuff/glove shadow
```

### Indices 14 and 15

A targeted diagnostic assigned:

```text
14 → cyan
15 → yellow
```

The unwanted robe highlights remained independently visible, ruling out `14` and `15` as their source. They remain part of Secondary.

### Index 56 — shared semantic index

Review of v1–v5 results established that index `56` simultaneously affects:

- a large visible area of the Secondary frock;
- sparse highlight pixels on the Primary robe.

This creates an unavoidable palette constraint: a single `.pal` entry cannot provide two different colors to those two sprite regions.

The production rule is therefore **adaptive color coordination**:

```text
if Primary and Secondary are similar in hue:
    56 ≈ coordinated Secondary highlight

if Primary and Secondary strongly contrast:
    56 = muted, darker Primary/Secondary bridge
```

The purpose is not mathematical midpoint accuracy. The purpose is to make `56` visually plausible in both regions.

### Current v5 male Acolyte map

```text
PRIMARY
73–79

SECONDARY
9,11,12,14,15

PRIMARY/SECONDARY BRIDGE
56

TERTIARY
13
49–55

QUATERNARY
1–2
10
16–23
25–31
65,66,68

OUTLINE / EDGE
43–48

ACCESSORY: BELT
81–89
normally Secondary-derived

NECK/COLLAR SHADOW
34,36,37,39,40
preserve

SPECIALIZED / UNRESOLVED
8
70–72
preserve
```

This is the recommended starting point for future male Acolyte palette generation.

---

## 25. Cross-class comparison plan — Male Thief

The next research target is the **male Thief** body sprite.

Do **not** assume the male Acolyte index map applies to Thief. Instead:

1. Obtain the exact male Thief `.spr` and `.act`.
2. Obtain at least one known-good modern male Thief `.pal` to use as a base.
3. Parse the Thief SPR to enumerate all used indices.
4. Compare its palette/index structure against male Acolyte.
5. Generate the same ten color themes.
6. Use contact sheets to determine whether Primary/Secondary/Tertiary/Quaternary families occupy the same or different index ranges.
7. Document the male Thief mapping independently.
8. Only after comparing multiple classes should any repeated mapping be considered a candidate cross-class convention.

The ten design themes to preserve are:

```text
1  Black / Crimson / Crimson-red / Oxblood
2  Black / Navy / Royal blue / Blue-black
3  Emerald / Brown / Warm lighter brown / Warm brown
4  Sky blue / Cloud white / Pale blue / Tan
5  Cream / Black / Warm taupe-brown / Dark brown
6  Black / Charcoal / Gold / Antique gold
7  Orange / Blue / Lighter blue / Dark brown
8  Purple / Black / White / Charcoal-violet
9  Charcoal / Dark charcoal / Medium charcoal / Near-black
10 Red / Crimson / Gold / Dark chestnut
```

Where each line is:

```text
Primary / Secondary / Tertiary / Quaternary
```
