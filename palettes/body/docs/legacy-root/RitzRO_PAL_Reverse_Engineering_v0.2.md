# Ragnarok Online `.pal` Reverse-Engineering Notes

**Version:** 0.2  
**Project context:** RitzRO / roBrowserLegacy / 2025 kRO client assets  
**Primary test sprite:** Male Acolyte (`성직자_남.spr`)  
**Status:** Experimental documentation. Binary findings, controlled visual diagnostics, and inferences are labeled separately.

## 1. Purpose

This document records reverse-engineering results for Ragnarok Online character `.pal` files and their relationship to indexed `.spr` sprites and `.act` animation files.

The immediate goal is to support an agent or developer creating a small set of deliberate, high-quality custom clothing palettes without corrupting skin, mounts, accessories, or unrelated sprite regions.

The detailed semantic mappings in this document apply specifically to the tested **male Acolyte body sprite** unless explicitly stated otherwise.

A central conclusion of v0.2 is that semantic labels such as **Primary**, **Secondary**, and **Tertiary** must be treated as **sprite/class-specific mappings**, not universal Ragnarok palette addresses.

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

1. **Palette/index semantics** — e.g. "male Acolyte Primary color family".
2. **Observed sprite usage** — e.g. "appears on robe, back yoke, cuffs, shoes".

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

### CORRECTION introduced in v0.2

In v0.1, the 177 entries that did not vary across these samples were informally treated as likely "protected".

That is too strong.

The correct conclusion is only:

> These entries were **invariant across the sampled palette pack**.

An invariant entry may still be clothing and may still need recoloring. Index `56` is now the key example: it did not vary in the sampled pack, but visual diagnostics show it participates in the stubborn cream chest/back region of the Acolyte outfit.

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

## 8. Diagnostics 707–709 — per-index color mapping

### 707 — indices `9–15`

```text
9  white
10 yellow
11 green
12 cyan
13 blue
14 magenta
15 red
```

Observed across:

- collar/back-panel details
- glove/hand-area clothing
- shoe/ankle accents
- other distributed trim pixels

The index order appears broadly consistent with a light→dark ramp.

Current classification:

```text
9–15 = Secondary color family / accent shading ramp
```

**Status:** CONFIRMED visual family; precise semantic distribution is sprite-specific.

---

### 708 — indices `45–55`

```text
45 white
46 yellow
47 green
48 cyan
49 azure
50 blue
51 violet
52 magenta
53 rose/pink
54 red
55 black
```

Observed around:

- glove/waist/lower-center details
- lower hem
- footwear/detail pixels

Usage is highly uneven. Known examples:

```text
43 → 3 pixels total
48 → 6 pixels total

53 → 8,503 pixels / all 110 frames
54 → 7,161 pixels / all 110 frames
55 → 5,091 pixels / all 110 frames
```

Current classification:

```text
40–55 = mixed clothing/detail family
```

The exact internal semantic split remains unresolved.

---

### 709 — indices `73–79`

```text
73 white
74 yellow
75 green
76 cyan
77 blue
78 magenta
79 red
```

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
73–79 = major male Acolyte Primary cloth ramp
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

## 9. Custom palette prototype v1 — IDs 9–18

Ten custom male Acolyte palettes were generated using:

```text
Primary:   73–79
Secondary: 9–15
Tertiary:  49–55
```

Schemes:

1. Black / Crimson
2. Black / Navy
3. Emerald / Brown
4. Sky Blue / Cloud White
5. Cream / Black
6. Black / Charcoal / Gold
7. Orange / Blue
8. Purple / Black / White
9. Charcoal
10. Red / Crimson / Gold

### Result

The main custom colors rendered successfully, but a persistent **cream/off-white chest region and rear upper-back/yoke patch** remained unchanged across the set.

This demonstrated that the visible Primary outfit is not fully represented by `73–79`.

---

## 10. Diagnostics 11 and 12 — testing indices 8 and 72

A v2 working hypothesis proposed:

```text
Secondary = 8–15
Primary   = 72–79
```

Two isolated diagnostics tested the leading entries.

### Diagnostic 11

```text
index 8 → green
```

Observed result:

- Green appears mainly on shoe/toe details in several side/diagonal directions.
- It is not the stubborn cream chest/back patch.

Current interpretation:

```text
index 8 = specialized footwear/detail usage
```

### Diagnostic 12

```text
index 72 → magenta
```

Observed result:

- No obvious magenta in the eight tested idle directions.
- The cream chest/back patch remains unchanged.

Current interpretation:

```text
index 72 = sparse/specialized usage, not the persistent cream chest/back region
```

### v2 hypothesis result

The simple assumption that `8–15` and `72–79` were complete unified ramps is **rejected**.

Preferred model remains:

```text
8      specialized detail
9–15   Secondary family

72     sparse/specialized
73–79  major Primary cloth ramp
```

---

## 11. Diagnostics 13 and 14 — locating the persistent cream patch

### Diagnostic 13 — broad candidate-family locator

Palette 13 recolored remaining used candidate families:

```text
16–23             GREEN
25–31             MAGENTA
34,36,37,39,40    CYAN
43–47             YELLOW
56                 BLUE
65,66,68           RED
70–71              ORANGE
81–89              VIOLET
```

### Critical result

The stubborn cream patch **did change**.

A prominent part of the rear upper-back/shoulder-blade patch turned **blue**.

Because blue was uniquely assigned to index `56`, this establishes:

> **Index 56 participates in the stubborn chest/rear-yoke color region.**

**Status:** CONFIRMED — visual diagnostic.

This corrects an earlier mistaken interpretation that diagnostic 13 had left the patch entirely unchanged.

### Diagnostic 14

Diagnostic 14 individually colored indices `16–23` and `25–31`.

Observed result:

- strong rainbow behavior on footwear
- scattered upper-body/detail pixels
- does not explain the main chest/back patch

This reduces the likelihood that `16–23` or `25–31` contain the principal missing Primary ramp.

---

## 12. Revised male Acolyte Primary model

The best current interpretation is:

```text
Male Acolyte Primary visual family
├── major ramp: 73–79
└── additional Primary-related entry/family: includes index 56
```

This means the visually unified robe/outfit is built from more than one palette region.

A custom generator must therefore avoid assuming:

```text
one semantic color = one contiguous PAL range
```

Instead, the correct model may be:

```text
Primary:
  Ramp/region A → 73–79
  Ramp/region B → includes 56, neighboring members still under investigation
```

Index `56` is a confirmed anchor for the second Primary-related region.

---

## 13. Diagnostic 15 — indices 43–56

**Status:** generated; visual test pending.

Every index `43–56` has been assigned a unique high-contrast color:

```text
43 white
44 yellow
45 lime
46 green
47 spring green
48 cyan
49 azure
50 blue
51 violet
52 magenta
53 rose
54 red
55 dark red
56 orange
```

Purpose:

- map the suspicious `43–56` neighborhood spatially
- isolate how `56` relates to nearby entries
- determine whether the cream chest/back region forms a second Primary ramp
- refine Secondary/Tertiary mappings for male Acolyte

Do not update final production ramps from diagnostic 15 until the visual test is complete.

---

## 14. Updated terminology

Use semantic color-family names instead of garment-specific labels.

Preferred terminology:

```text
Primary
Secondary
Tertiary
Quaternary (if needed)
Protected / fixed only when independently established
```

Example:

```text
Primary
    dominant intended outfit color family

Secondary
    major contrasting family

Tertiary
    smaller trim/detail family
```

Do not define "Primary" universally as `73–79`.

Instead document:

```text
Male Acolyte:
    Primary includes 73–79 and index 56-related region
    Secondary includes 9–15
    Tertiary currently unresolved/mixed around 40–55
```

Another class may use completely different palette indices.

---

## 15. Class-specific mapping rule

Open-source Ragnarok palette/sprite tools support a sprite-specific workflow rather than a universal hardcoded color map.

Relevant tools/projects reviewed:

- `ragassets`
- ActEditor
- actOR / Ragnarok.Tools
- RagLite / RagnarokResearchLab
- RagnarokFileFormats

The practical lesson is:

> **Palette-index semantics belong to the specific SPR, not to Ragnarok globally.**

Therefore maintain mappings per body sprite/class/sex/variant.

Recommended future documentation structure:

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

## 16. ACT-aware findings

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

## 17. Example idle-direction index sets

### South-facing idle

```text
1–15:
2, 9, 10, 11, 13, 14

40–55:
45, 47, 49, 50, 51, 52, 53, 54, 55

72–79:
73, 74, 75, 76, 77, 78, 79

88–95:
none
```

### North-facing idle

```text
1–15:
9, 11, 12, 14, 15

40–55:
46, 47, 52, 53, 54, 55

72–79:
73, 74, 75, 76, 77, 78, 79

88–95:
89
```

---

## 18. Current male Acolyte working map

```text
8
    specialized footwear/detail usage
    CONFIRMED visual diagnostic

9–15
    Secondary/accent shading family
    distributed across collar/back/gloves/footwear
    broadly light → dark
    CONFIRMED visual family / ordering partly inferred

40–55
    mixed clothing/detail family
    exact Primary/Secondary/Tertiary split unresolved
    CONFIRMED used; semantics incomplete

56
    participates in persistent cream chest/rear-yoke region
    likely Primary-related
    CONFIRMED visual diagnostic

72
    sparse/specialized
    not visible in tested 8-direction idle contact sheet
    CONFIRMED binary; visual semantics unresolved

73–79
    major Primary cloth shading ramp
    73 brightest → 79 darkest
    CONFIRMED visual family; ordering strongly inferred

81–89
    specialized/detail/action-dependent family
    semantics incomplete

112–127
168–175
192–199
    unused by male Acolyte SPR
    CONFIRMED binary
```

---

## 19. Rules for custom palette generation

For the male Acolyte sprite:

1. Start from a known-good modern palette.
2. Preserve every byte except deliberately targeted RGB values.
3. Preserve the fourth byte of each palette entry.
4. Parse SPR usage before editing indices.
5. Treat Primary/Secondary/Tertiary as sprite-specific semantic families.
6. Do not assume a semantic family is contiguous.
7. Use `73–79` for the major Primary robe ramp.
8. Include the index-56-related region when it is fully mapped; otherwise custom Primary recolors will retain cream patches.
9. Use `9–15` as the currently best-understood Secondary family.
10. Treat `40–55` cautiously until diagnostic 15 resolves its internal structure.
11. Do not recolor unused ranges simply because another palette pack varies them.
12. Do not equate "unchanged across sample palettes" with "protected".
13. Validate all production palettes with at least an eight-direction contact sheet.
14. For rare/action-specific indices, use ACT-aware rendering or testing.

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
8. Assign sprite-specific semantic families:
   - Primary
   - Secondary
   - Tertiary
   - additional families as needed
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

Established through an isolated known-color test.

Example:

> Index `56` participates in the male Acolyte rear upper-back color region.

### INFERRED

Strongly suggested but not uniquely proven.

Example:

> Index `56` belongs to a second Primary shading family.

### UNKNOWN

Not yet established.

---

## 22. Current next step

Complete visual testing of **Diagnostic 15 (`43–56`)**.

Use an eight-direction contact sheet.

Primary questions:

1. Which indices in `43–56` occupy the chest/rear-yoke patch?
2. Is `56` part of a contiguous or noncontiguous Primary shading family?
3. Which entries belong to Secondary/Tertiary details instead?
4. Can the male Acolyte generator be revised so Primary recolors cover the entire visually unified robe/outfit?

After diagnostic 15 is interpreted, update this document to v0.3 and generate the next production palette revision.

---

## 23. Core methodology

> **Parse first, recolor second, visually label third.**

Binary SPR/ACT analysis establishes what can be affected and when it appears. Controlled diagnostics establish what those used indices mean visually. Production palette generation comes only after those two steps.
