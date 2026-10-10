# Ragnarok Online `.pal` Reverse-Engineering Notes

**Version:** 0.1\
**Project context:** RitzRO / roBrowserLegacy / 2025 kRO client assets\
**Primary test sprite:** Male Acolyte (`성직자_남.spr`)\
**Status:** Experimental documentation. Distinguish confirmed binary
facts from sprite-specific visual interpretation.

## 1. Purpose

This document records the current reverse-engineering results for
Ragnarok Online character `.pal` files and their relationship to indexed
`.spr` sprites and `.act` animation files.

The immediate goal is to support an agent or developer creating a small
set of deliberate, high-quality custom clothing palettes without
corrupting skin, mounts, accessories, or other sprite regions.

This is **not** yet a universal palette map for all Ragnarok jobs. The
detailed semantic mappings in v0.1 apply specifically to the tested
**male Acolyte body sprite** unless explicitly stated otherwise.

## 2. Rendering model

The useful mental model is:

``` text
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

A palette entry is **not inherently a semantic object** such as "shoe",
"robe", or "glove". A sprite contains pixels that reference palette
indices. The sprite artist may reuse the same color ramp across
disconnected regions such as the collar, gloves, back panel, and
footwear.

Therefore documentation should distinguish:

1.  **Palette semantics** --- e.g. "primary seven-step cloth shading
    ramp".
2.  **Observed sprite usage** --- e.g. "on male Acolyte this ramp
    appears on the robe/trousers".

## 3. `.pal` file structure

### Confirmed from tested files

Every tested palette file is exactly:

``` text
1024 bytes
```

The working model is:

``` text
256 entries × 4 bytes = 1024 bytes
```

There is no observed header or compression in these standalone `.pal`
files.

Entry offsets are:

``` text
entry 0   → bytes 0–3
entry 1   → bytes 4–7
...
entry 255 → bytes 1020–1023
```

In the tested files, editing the first three bytes of an entry changes
its visible RGB color. The fourth byte has been preserved during
diagnostic edits rather than rewritten.

**Agent rule:** when recoloring a known-good palette, modify RGB bytes
only unless/until the fourth byte's semantics are separately verified.

## 4. SPR/ACT test assets

The current reference sprite is the normal male Acolyte body:

``` text
data\sprite\인간족\몸통\남\성직자_남.spr
```

The matching ACT is:

``` text
data\sprite\인간족\몸통\남\성직자_남.act
```

Current analysis found:

-   SPR version: **2.1**
-   Indexed SPR frames: **110**
-   Truecolor frames: **0**
-   ACT version: **2.5**
-   ACT actions: **104**
-   The ACT references all 110 indexed SPR frames.
-   The action set is organized as 13 animation groups × 8 directions.

The useful direction order is:

``` text
S, SW, W, NW, N, NE, E, SE
```

## 5. Actual palette-index usage in male Acolyte SPR

Parsing all 110 indexed frames shows that only **66 nontransparent
palette indices** are referenced:

``` text
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

Any palette entry outside the set above cannot affect this specific SPR,
regardless of what RGB value is stored in the `.pal`.

This is an important distinction from comparing palette files: a palette
pack may vary entries that a particular sprite never references.

## 6. Initial multi-palette comparison

Nine known-good male Acolyte clothing palettes were compared:

``` text
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

Across those files, only 79 of 256 palette entries varied:

``` text
1–15
40–55
72–79
88–95
112–127
168–175
192–199
```

The other 177 entries were identical across the nine samples.

This comparison identified candidate recoloring blocks, but SPR parsing
later proved that some candidate blocks are not referenced by the male
Acolyte sprite.

## 7. Diagnostic experiment 700--706

Palette 692 was used as a known-good base. Seven test palettes were
created by replacing one candidate block at a time with a screaming
solid color.

  --------------------------------------------------------------------------
  Test           Modified entries Diagnostic    Binary usage  Visual result
                                  color         in Acolyte    
                                                SPR           
  ------------- ----------------- ------------- ------------- --------------
  700                      `1–15` Magenta       `1,2,8–15`    Strong visible
                                                used          effect

  701                     `40–55` Green         `40,43–55`    Strong visible
                                                used          effect

  702                     `72–79` Cyan          all 8 used    Very strong
                                                              visible effect

  703                     `88–95` Yellow        only `88–89`  Small/subtle
                                                used          effect

  704                   `112–127` Red           none used     No legitimate
                                                              effect
                                                              possible

  705                   `168–175` Blue          none used     No effect
                                                              possible

  706                   `192–199` Orange        none used     No effect
                                                              possible
  --------------------------------------------------------------------------

### Important correction produced by binary analysis

An earlier screenshot comparison suggested palette 704 might have caused
a subtle change. SPR parsing disproved that interpretation: the male
Acolyte SPR contains **zero pixels** referencing indices `112–127`.

Therefore any apparent difference in test 704 was visual
ambiguity/noise.

**Agent rule:** binary SPR index usage overrides subjective screenshot
inference about whether an index is used.

## 8. Front/rear observations from 700--706

### `1–15`

Observed on male Acolyte in:

-   upper garment/collar
-   upper-back panel
-   glove/hand-area clothing
-   shoe/ankle accents

This is a distributed accent/detail family, not a single body part.

### `40–55`

Observed on:

-   lower garment/trousers
-   portions of sleeves/arms
-   lower hem
-   footwear/details

This family contains both extremely sparse indices and heavily used
indices.

### `72–79`

Observed across:

-   major sleeves
-   large trouser/robe regions
-   very large rear lower-body/robe region

This is the clearest **primary cloth color family** for the male
Acolyte.

### `88–95`

Only indices `88–89` are used by the SPR.

-   `88` is exceptionally specialized.
-   `89` has broader but still comparatively limited usage.
-   The block is not a general-purpose eight-color clothing ramp for
    this sprite.

### `112–127`, `168–175`, `192–199`

Not referenced by the male Acolyte SPR.

Do not spend effort recoloring these ranges for this sprite.

## 9. Targeted diagnostic experiment 707--709

Three new diagnostic palettes assigned a unique screaming color to
**each individual index** in important ranges.

### Palette 707 --- indices `9–15`

``` text
9  → white
10 → yellow
11 → green
12 → cyan
13 → blue
14 → magenta
15 → red
```

Observed usage is distributed across collar/back-panel/glove/footwear
regions.

The visual progression is consistent with a **light-to-dark shading ramp
as the index increases**.

Current interpretation:

``` text
9  → brightest
10
11
12
13
14
15 → darkest
```

This should be described as an **accent shading ramp**, not as seven
independent semantic body parts.

### Palette 708 --- indices `45–55`

``` text
45 → white
46 → yellow
47 → green
48 → cyan
49 → light blue
50 → blue
51 → violet
52 → magenta
53 → pink
54 → red
55 → black
```

Visible pixels are concentrated around glove/waist/lower-center details
from the front, with additional lower-hem and footwear use from the
rear.

The range is not uniformly important. Binary usage shows some entries
are extremely sparse while `53–55` are major workhorse colors.

Known examples:

``` text
43 → 3 pixels total
48 → 6 pixels total

53 → 8,503 pixels / all 110 frames
54 → 7,161 pixels / all 110 frames
55 → 5,091 pixels / all 110 frames
```

Treat `40–55` as a mixed secondary/detail color family until finer
structural analysis is completed.

### Palette 709 --- indices `73–79`

``` text
73 → white
74 → yellow
75 → green
76 → cyan
77 → blue
78 → magenta
79 → red
```

This test strongly confirms `73–79` as the principal seven-step male
Acolyte cloth shading ramp.

Current mapping:

``` text
73 → brightest highlight
74 → highlight
75 → light
76 → midtone
77 → shadow
78 → deep shadow
79 → darkest shade
```

This ordering is supported by the diagnostic screenshots and by
widespread usage across the sprite.

## 10. Primary cloth ramp usage counts

Across all 110 indexed SPR frames:

    Index   Total pixels   Frames containing index
  ------- -------------- -------------------------
       72            125                        26
       73          1,917                        68
       74         10,513                       110
       75         18,614                       110
       76         20,905                       110
       77          7,304                       110
       78          3,791                       108
       79          5,535                       110

Indices `74–79` are core clothing colors. `72–73` are more specialized,
with `72` especially sparse.

For deliberate custom palettes, `73–79` is currently the best-understood
region to edit.

## 11. ACT-aware findings

ACT analysis explains why visual testing of a single idle direction can
miss legitimate palette usage.

A notable example is index `88`:

``` text
index 88
→ appears in only one SPR frame (frame 79)
→ that frame is referenced by Frozen/Stun actions
→ observed for W, NW, N, and NE orientations
```

Thus a front-facing idle screenshot is insufficient to determine whether
a palette index is globally unused.

**Agent rule:** use full SPR/ACT analysis to determine index usage.
Screenshots are for assigning semantic meaning to already-confirmed used
pixels.

## 12. Example idle-direction index sets

### South-facing idle

Observed/referenced indices from important families include:

``` text
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

``` text
1–15:
9, 11, 12, 14, 15

40–55:
46, 47, 52, 53, 54, 55

72–79:
73, 74, 75, 76, 77, 78, 79

88–95:
89
```

This explains why some diagnostic colors appear only from particular
orientations.

## 13. Rules for custom palette generation

For the **male Acolyte sprite**, an editing agent should currently
follow these rules:

1.  Start from a known-good modern palette compatible with the current
    sprite.
2.  Preserve the entire 1024-byte palette except for deliberately
    targeted RGB entries.
3.  Do not assume every palette entry is referenced by the sprite.
4.  Consult SPR index usage before editing a range.
5.  Treat palette entries as **color ramps**, not semantic body parts.
6.  For a basic primary clothing recolor, target `73–79`.
7.  Construct `73–79` as a smooth light-to-dark ramp.
8.  Preserve hue relationships while decreasing luminance/value through
    the ramp.
9.  Treat `9–15` as a secondary/accent shading ramp.
10. Treat `40–55` as a mixed secondary/detail family requiring more
    caution.
11. Do not edit `112–127`, `168–175`, or `192–199` for male Acolyte; the
    SPR does not reference them.
12. Do not assume these mappings apply to another job, sex, mounted
    sprite, head sprite, or garment.
13. Preserve the fourth byte of each `.pal` entry until its semantics
    are independently verified.
14. Validate generated palettes against the actual SPR/ACT, not merely
    against another palette file.

## 14. Generalization strategy for other jobs

Do **not** manually reproduce the Acolyte experiment for every class.

Instead:

1.  Obtain the target `.spr`.
2.  Parse all indexed frames.
3.  Enumerate every palette index referenced by each frame.
4.  Obtain the matching `.act`.
5.  Map SPR frames to actions/directions.
6.  Compare the target sprite's used indices against known-good palette
    variants.
7.  Generate diagnostic renders/contact sheets where necessary.
8.  Use manual screenshots only to attach semantic labels such as
    "robe", "boot", "mount", or "saddle".

For mounted classes, compare the unmounted and mounted sprite index
usage. New ranges introduced by the mounted sprite are candidates for
mount-specific colors, but semantic classification still requires
pixel-level or visual validation.

## 15. Public-tool/source direction

Public Ragnarok tooling indicates that sprite-specific analysis is the
correct approach.

Relevant projects investigated during this work include:

-   **ragassets** --- SPR/ACT/PAL rendering and sprite-specific
    skin-index analysis, including special handling for mounts and
    multiple skin ramps.
-   **ActEditor** --- open-source ACT/SPR editing and palette tooling.
-   **RagLite / RagnarokResearchLab** --- file-format decoding and
    research tooling.
-   **RagnarokFileFormats** --- public documentation for SPR and ACT
    structures.

The important design lesson from these tools is that palette semantics
are **sprite-specific**. A universal statement such as "indices X--Y are
always skin" is unsafe.

## 16. Known unknowns / next experiments

### Palette format

-   Verify the exact semantics of the fourth byte in standalone `.pal`
    entries.
-   Confirm whether index 0 has special/transparency behavior in
    standalone palettes versus SPR rendering.

### Male Acolyte

-   Refine the internal structure of `40–55`.
-   Determine the exact role of sparse indices such as `43`, `48`, `72`,
    and `88`.
-   Generate programmatic diagnostic renders from SPR pixels instead of
    relying on in-game testing.
-   Determine whether the light-to-dark ordering inferred for `9–15` and
    `73–79` holds in every relevant animation.

### Cross-sprite analysis

-   Analyze female Acolyte.
-   Analyze an unmounted class with different clothing geometry.
-   Analyze Knight and Peco Knight as a paired mounted/unmounted case.
-   Determine which palette concepts generalize across jobs and which
    are sprite-specific.
-   Investigate head/hair palettes separately from body palettes.

## 17. Confidence terminology

Future revisions should label findings using these categories:

### CONFIRMED --- binary

Directly established from file structure or parsed SPR/ACT data.

Example:

> Male Acolyte SPR never references palette indices 112--127.

### CONFIRMED --- visual diagnostic

Established by a controlled palette experiment where a known index/range
was assigned a unique diagnostic color and observed in-game.

Example:

> Male Acolyte indices 73--79 affect the main cloth region.

### INFERRED

Strong interpretation supported by diagnostics but not uniquely proven.

Example:

> Index order 73→79 represents brightest→darkest shading.

### UNKNOWN

Not yet established.

This terminology should be retained so future agents do not silently
promote an inference into a fact.

## 18. Current working summary

For male Acolyte body palettes, the most useful current model is:

``` text
9–15
    Secondary/accent shading ramp
    distributed across collar/back/gloves/footwear
    approximately light → dark

40–55
    Mixed secondary/detail clothing family
    contains both sparse and heavily used entries
    needs further decomposition

73–79
    PRIMARY CLOTH SHADING RAMP
    73 brightest → 79 darkest
    high-confidence target for custom recoloring

88–89
    sparse/specialized detail usage
    action/direction dependent

112–127
168–175
192–199
    unused by male Acolyte SPR
```

The central methodological rule is:

> **Parse first, recolor second, visually label third.**

SPR/ACT analysis determines what can actually be affected. Controlled
palette diagnostics determine what those used indices correspond to
visually. Only then should custom color ramps be generated.
