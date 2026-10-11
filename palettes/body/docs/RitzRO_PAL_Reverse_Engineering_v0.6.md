# Ragnarok Online Palette Reverse-Engineering and Generation Guide

**Version:** 0.6  
**Project context:** RitzRO / roBrowserLegacy / 2025 kRO client assets  
**Validated reference sprites:** Male Acolyte (`성직자_남.spr`) and Male Thief (`도둑_남.spr`)  
**Status:** Working technical guide. The generalized procedure is the primary document; sprite-specific mappings are retained as appendices and cached analysis results.

---

## 1. Purpose

This document describes a reusable method for analyzing Ragnarok Online body sprites and generating deliberate, high-quality clothing palettes.

The central design goal is **not** to build one universal hardcoded palette-index table. Palette indices are properties of a specific indexed `.spr` file, and the same numerical index can represent different visual regions in different jobs, sexes, mounts, or client asset revisions.

Instead, the recommended workflow is:

```text
SPR + ACT + known-good PAL
        ↓
structural decoding
        ↓
spatial / frame / action analysis
        ↓
semantic interpretation
        ↓
Primary / Secondary / Tertiary / etc. grouping
        ↓
shared-index detection
        ↓
color-theory-aware palette generation
        ↓
visual validation
        ↓
cached sprite-specific mapping keyed to exact asset identity
```

Existing Acolyte and Thief tables remain valuable, but they should be treated as **cached outputs of this procedure**, not as universal rules.

---

## 2. Core rendering model

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

A palette entry is not inherently a semantic object such as "jacket," "robe," "boot," or "glove." It is only a color referenced by one or more indexed pixels.

The same palette index may appear:

- across one coherent garment region;
- in several disconnected parts of the same garment;
- in entirely different semantic regions;
- in only one animation or direction;
- as a major fill region in one place and a few sparse highlight pixels somewhere else.

Therefore semantic meaning must be **inferred from observed sprite usage**, not assumed from index number or contiguity.

---

## 3. `.pal` file structure

### Confirmed from tested assets

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

Editing the first three bytes changes visible RGB color. The fourth byte has been preserved during all successful diagnostics and production edits.

**Generation rule:** modify RGB bytes only unless the fourth byte has been independently understood for the target client format.

---

# Part I — Generalized Asset Analysis

## 4. Analyze the exact target assets, not the job name

Mappings should be associated with the exact body sprite variant, ideally by hash.

Recommended identity record:

```text
job: Thief
sex: male
sprite_path: data/sprite/.../도둑_남.spr
spr_sha256: ...
act_sha256: ...
base_pal_sha256: ...
client_asset_set: 2025 kRO / RitzRO
```

Why this matters:

- a different client version can contain a changed sprite under the same filename;
- male/female variants are independent;
- mounted/unmounted variants may be independent;
- reused job names do not guarantee identical indexed artwork.

When an exact sprite hash is already present in the mapping library, an agent can reuse the cached semantic table. Otherwise, it should run the generalized analysis procedure.

---

## 5. Parse the SPR first

For every indexed frame, decode the palette-index raster and collect at minimum:

```text
frame number
frame width / height
palette indices used
pixel count per index
pixel coordinates per index
bounding box per index
connected components per index
```

Across the entire sprite, aggregate:

```text
total pixel count per index
number of frames containing each index
per-frame pixel counts
normalized x/y distribution
upper-body vs lower-body usage
left/right distribution
component-size distribution
```

This immediately answers questions that palette-file comparison alone cannot answer:

- Which indices are actually referenced?
- Which indices dominate the visible clothing?
- Which indices are rare or action-specific?
- Which indices are concentrated on torso, hands, legs, or feet?
- Which indices appear as one coherent patch versus many disconnected speckles?

### Binary rule

If an index does not occur in the SPR, changing it cannot affect that sprite.

Binary SPR usage overrides subjective screenshot impressions about whether an index is active.

---

## 6. Use spatial analysis, not just index ranges

Numerically adjacent indices often form ramps, but this is not guaranteed.

For each used index, inspect:

- bounding box;
- centroid;
- upper / middle / lower body concentration;
- connected component count;
- component sizes;
- overlap with neighboring indices;
- co-occurrence across the same frames.

Useful interpretation patterns:

### A. Large coherent component

Often indicates a major garment area.

Example pattern:

```text
index 76
→ thousands of pixels
→ centered on torso
→ appears in nearly every frame
```

Likely candidate for a main cloth ramp.

### B. Large component plus sparse distant components

Strong warning for a **shared semantic index**.

Example pattern:

```text
index 40
→ large chest patch
→ several 1–3 pixel shoulder clusters
```

This means one color must satisfy both visual roles.

### C. Lower-body-only concentration

Often indicates footwear, pants, knees, or leg accessories.

### D. Tiny rare components in only a few frames

Likely action-specific, effect-adjacent, or specialized detail pixels. Preserve until understood.

---

## 7. Parse the ACT second

SPR analysis answers **where an index exists**. ACT analysis answers **when and how it appears in-game**.

For each ACT action and animation frame, record:

```text
action number / name if known
direction
referenced SPR frame
layer order
offsets
```

Then map palette-index usage back to:

- idle directions;
- walking;
- attacking;
- hit / hurt;
- death;
- sit;
- status poses;
- any rare class-specific actions.

This prevents an index from being incorrectly dismissed just because it is absent from an idle screenshot.

Example from Acolyte work:

```text
index 88
→ appears in a rare SPR frame
→ still matters because ACT references that frame in status actions
```

---

## 8. Compare known-good palettes only as supporting evidence

Multiple known-good `.pal` files are useful for identifying which entries tend to vary together, but variation is not the same as semantic meaning.

Use palette comparison to ask:

```text
Which indices vary across official/custom palettes?
Which entries move together as apparent ramps?
Which entries remain invariant?
```

Do **not** conclude:

```text
invariant = protected
```

The Acolyte work disproved that assumption. An index can remain unchanged across a sample pack and still be part of clothing.

Preferred terminology:

```text
INVARIANT IN SAMPLE SET
```

Use "protected" only after independent evidence shows that an index should not be recolored.

---

# Part II — Semantic Interpretation

## 9. Semantic families are visual design roles, not fixed index ranges

The standard names are:

```text
Primary
Secondary
Tertiary
Quaternary
Outline / Edge
Accessory
Bridge / Shared
Protected / Fixed
Unresolved / Preserve
```

These labels describe **design function**, not numerical location.

A practical interpretation is:

- **Primary** — largest or most visually dominant garment family.
- **Secondary** — second major clothing region.
- **Tertiary** — distinct smaller garment or trim family, often gloves/shoes/cuffs.
- **Quaternary** — additional coordinated detail family.
- **Outline / Edge** — structural darks defining shape and boundaries.
- **Accessory** — belt, kneepad, undershirt, trim, ornament, etc.
- **Bridge / Shared** — one index physically reused across semantic regions.
- **Protected / Fixed** — independently established as something that should remain unchanged.
- **Unresolved / Preserve** — used, but not yet understood well enough to recolor safely.

The semantic assignment should follow the artwork, not force every sprite into the same garment interpretation.

---

## 10. Use human/agent judgment to split visual regions

After structural decoding, render the sprite or index maps and ask:

```text
What are the visually distinct clothing areas?
Which regions should read as one material?
Which regions should contrast?
Which colors define silhouette versus detail?
Which regions are skin/hair-adjacent and therefore risky?
```

The agent should group indices by **visual region and material behavior**, not merely by numerical range.

Examples:

```text
16–23 may form one pants ramp.
24–39 may collectively form gloves/shoes.
40 may need to stand alone because it is shared.
41–47 may remain a separate undershirt ramp.
```

A contiguous range may need to be split if its spatial usage crosses garment boundaries.

---

## 11. Detect shared indices explicitly

Shared indices are one of the most important lessons from the project.

A shared index is an index whose pixels belong to two or more visually different semantic regions.

Detection signals include:

- one large connected component plus several small distant components;
- strong use in one body zone and sparse use in another;
- in-game "color bleed" that follows exactly one index;
- a color that fixes one garment but introduces obvious artifacts elsewhere.

Examples discovered so far:

```text
Male Acolyte index 56
→ substantial Secondary frock region
→ sparse Primary robe highlights

Male Thief index 40
→ large undershirt/chest region
→ sparse jacket/shoulder highlights

Male Thief index 9
→ jacket highlight usage
→ small footwear usage
```

### Shared-index production rule

Do not force a shared index into one pure family if that makes the other region look wrong.

Instead choose a **bridge color** that is visually plausible in both uses.

General approach:

```text
if the two semantic families are similar:
    bias toward the family containing the dominant component

if the two families strongly contrast:
    reduce saturation
    avoid extreme brightness
    bias value toward a middle or darker compromise
    preserve enough hue relationship to read as intentional in both regions
```

The goal is not a mathematical midpoint. The goal is a sprite-quality compromise.

---

## 12. Numerical contiguity is not semantic contiguity

Do not assume:

```text
72–79 = one garment ramp
```

simply because the indices are adjacent.

The Thief work showed that:

```text
72–74 = footwear detail
75–79 = jacket main
```

Likewise, Acolyte ranges required semantic boundaries inside larger candidate blocks.

Therefore every suspected ramp should be validated by spatial use, visual tests, or both.

---

# Part III — Diagnostic Rendering

## 13. Generate diagnostic index maps

A reusable analysis tool should support rendering the sprite with selected palette indices replaced by unmistakable diagnostic colors.

Useful modes:

### Single-index mode

```text
index 40 → magenta
all others → original palette
```

Best for confirming one ambiguous index.

### Range mode

```text
40–47 → green
```

Best for locating broad candidate regions.

### Individual rainbow mode

Assign a unique screaming color to every index in a candidate range.

Best for finding semantic boundaries inside a numerical range.

### Semantic-family preview

Apply provisional Primary/Secondary/Tertiary colors to test whether the inferred grouping matches the artwork.

---

## 14. Produce contact sheets, not one screenshot

Minimum validation should include:

```text
8 idle directions
```

Better validation includes:

```text
idle
walk
attack
hurt
sit
status/death poses where practical
```

A mapping is not production-ready simply because the south-facing idle frame looks correct.

---

# Part IV — Color Theory and Sprite Quality

## 15. Correct indexing is necessary but not sufficient

A technically correct mapping can still produce a poor palette.

The v3 Thief palettes demonstrated this clearly: jacket and gloves could be correctly mapped to different semantic families yet still visually merge because their hues and values were too similar.

Production palettes must therefore optimize both:

```text
index correctness
+
visual separation / harmony
```

---

## 16. Preserve readable ramps

Each semantic family should retain visible internal shading.

Avoid ramps where:

- all values collapse into near-black;
- highlights clip to white;
- adjacent entries become nearly identical;
- shadows are so saturated that they read as unrelated colors.

Dark palettes are especially vulnerable. "Black" clothing usually looks better as a very dark colored ramp rather than repeated RGB values near zero.

Example principle learned from Thief styles 1–2:

> Pants can still read as black while retaining enough value separation for folds and sprite detail to remain visible.

---

## 17. Separate major garment families deliberately

Primary/Secondary/Tertiary labels should have useful visual distinction unless the intended style is intentionally monochrome.

Good separation can come from:

- hue contrast;
- value contrast;
- saturation contrast;
- material logic.

Examples from Thief v4:

```text
crimson jacket + leather gloves
navy jacket + cognac gloves
blue jacket + brown boots
```

These read more clearly than:

```text
crimson jacket + crimson gloves
navy jacket + blue gloves
```

Coordination is desirable. Duplication is not always desirable.

---

## 18. Keep outlines functional

Outline / edge families should usually remain darker and more muted than the surfaces they define.

Their job is to:

- preserve silhouette;
- separate overlapping garment regions;
- keep the sprite readable against variable maps/backgrounds.

Do not brighten outline families merely because the palette theme is bright.

---

## 19. Use material logic

Where the sprite clearly implies different materials, color design should respect that visual language.

Examples:

- leather gloves/boots can use warmer browns than cloth jackets;
- undershirts can be lighter and lower-saturation;
- metal trim can use restrained high-value neutrals;
- belts/accessories can coordinate with Secondary or Tertiary without becoming identical.

This is a design judgment layer beyond binary decoding.

---

## 20. Shared-index color theory

For shared indices, extreme colors are dangerous.

Avoid:

```text
pure white
high-saturation accent colors
maximum-value highlights
```

unless both semantic regions can tolerate them.

Preferred shared-index colors are often:

```text
lighter than the main garment midtone
less saturated than either main family
slightly biased toward the visually dominant region
```

This is exactly why Thief index 40 improved when changed from near-white to a pale jacket-tinted bridge.

---

# Part V — Recommended Agent Workflow

## 21. Reusable end-to-end procedure

For an unseen job/body sprite, the agent should follow this sequence.

### Step 1 — identify exact assets

Obtain:

```text
SPR
ACT
at least one known-good matching PAL
```

Hash them.

### Step 2 — check cache

If exact SPR hash already has a validated mapping:

```text
reuse mapping
verify ACT/base PAL compatibility
```

Otherwise continue.

### Step 3 — decode SPR

Generate:

- used-index list;
- pixel counts;
- frame counts;
- coordinates;
- bounding boxes;
- connected components;
- body-zone distributions.

### Step 4 — decode ACT

Map frames to actions/directions and identify rare/action-specific indices.

### Step 5 — compare known-good palettes

Use variation patterns as supporting evidence only.

### Step 6 — create diagnostic renders

Start broad, then narrow ambiguous ranges.

### Step 7 — assign provisional semantic families

Use visual clothing areas and material logic to define:

```text
Primary
Secondary
Tertiary
Quaternary
Accessory
Outline
Bridge
Preserve
```

### Step 8 — inspect for shared indices

Flag indices whose connected components or body-zone use cross semantic regions.

### Step 9 — generate trial palette

Use color theory, readable ramps, and semantic separation.

### Step 10 — validate

Inspect multiple directions/actions.

### Step 11 — refine

If a defect appears:

```text
identify exact affected pixels
trace them back to palette index
check whether that index is dedicated or shared
adjust semantic table or bridge rule
```

### Step 12 — cache the result

Save the validated mapping under the exact SPR hash, along with confidence notes.

---

## 22. Suggested machine-readable analysis output

A future analysis script should ideally emit structured data similar to:

```yaml
sprite:
  sha256: ...
  frames: 116

indices:
  40:
    pixels_total: ...
    frames_used: ...
    bbox_global: ...
    connected_component_profile: ...
    upper_body_ratio: ...
    lower_body_ratio: ...
    semantic_status: shared
    semantic_labels:
      - undershirt
      - jacket_highlight

  73:
    pixels_total: 3022
    frames_used: 115
    lower_body_ratio: high
    semantic_status: provisional
    semantic_labels:
      - footwear_detail
```

This allows an agent to reason from evidence while still keeping a human-readable table.

---

## 23. Confidence model

Use explicit confidence labels.

### CONFIRMED — binary

Directly established from decoded file data.

Example:

> index 73 occurs 3,022 times across 115 Thief frames.

### CONFIRMED — controlled visual diagnostic

Established by targeted recoloring and visual verification.

### STRONGLY INFERRED

Structural and visual evidence agree, but no single-index diagnostic has fully isolated the role.

### PROVISIONAL

Current best production assignment, still subject to additional action/direction testing.

### UNKNOWN / PRESERVE

Used, but not understood well enough to recolor safely.

---

## 24. What the agent should not do

Do not:

- copy one job's mapping to another job;
- assume male/female variants share indices;
- infer garment roles from numerical contiguity alone;
- call invariant palette entries "protected" without evidence;
- judge an index only from one front-facing frame;
- make shared indices pure white or highly saturated by default;
- sacrifice readable shading merely to hit a named color such as "black";
- recolor unknown skin/hair-adjacent indices casually;
- discard prior validated mappings once the generalized workflow exists.

The generalized procedure and the cached tables are complementary.

---

# Part VI — Cached Reference Mappings

These mappings are retained as validated or working outputs of the generalized process. They are **not universal Ragnarok index conventions**.

## Appendix A — Male Acolyte

### Asset facts

```text
SPR version: 2.1
indexed frames: 110
ACT version: 2.5
ACT actions: 104
```

Used nontransparent indices observed in the tested SPR:

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

### Current working semantic map

```text
PRIMARY
73–79

SECONDARY
9,11,12,14,15

PRIMARY / SECONDARY BRIDGE
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

NECK / COLLAR SHADOW
34,36,37,39,40
preserve

SPECIALIZED / UNRESOLVED
8
70–72
preserve
```

### Key shared-index lesson: index 56

```text
56
→ substantial Secondary frock region
→ sparse Primary robe highlights
```

Production rule:

```text
if Primary and Secondary are similar:
    use a coordinated Secondary highlight

if strongly contrasting:
    use a muted, darker bridge
```

### Important Acolyte corrections from iteration

```text
10 → Quaternary shoe highlight
13 → Tertiary cuff/glove shadow
14–15 → Secondary
43–48 → structural outline / edge
49–55 → Tertiary
```

---

## Appendix B — Male Thief

### Asset facts

Tested male Thief SPR contains:

```text
116 indexed frames
```

### Current working semantic map

```text
PRIMARY — PANTS
16–23

SECONDARY — JACKET HIGHLIGHTS
9,10
57–63

SECONDARY — JACKET MAIN
75–79

TERTIARY — GLOVES / SHOES
24–39

FOOTWEAR DETAIL
72–74
normally derive from Tertiary / boot color

SHARED JACKET / FOOTWEAR HIGHLIGHT
9

SHARED UNDERSHIRT / JACKET HIGHLIGHT
40

UNDERSHIRT / LIGHT DETAILS
41–47

KNEEPAD / ACCESSORY DETAILS
48–55

QUATERNARY — REAR / BACK BOOT PANELS
64–71
```

### Index 40 lesson

Decoded frame data showed:

```text
40
→ large central chest / undershirt component
→ multiple tiny jacket / shoulder components
```

Therefore:

```text
40 = light Secondary / Accessory bridge
41–47 = actual light undershirt/detail ramp
```

Do not make 40 near-white unless the jacket can tolerate white highlights.

### Footwear / jacket split lesson

Fresh SPR analysis corrected the earlier assumption that `72–79` was one jacket family.

In the representative south-facing standing frame:

```text
75–79 → jacket
73    → large right-boot patch
72    → tiny adjacent boot highlight
9     → additional shared jacket/footwear pixels
```

Across the full 116-frame SPR:

```text
index 73
→ 3,022 pixels
→ 115 frames
→ overwhelmingly lower-body concentrated
```

Current production interpretation:

```text
72–74 = footwear detail
75–79 = jacket main
9     = shared jacket / footwear detail
```

### Tertiary separation lesson

Earlier palettes sometimes used nearly identical jacket and glove hues, causing garment families to merge visually.

Better examples:

```text
Crimson jacket / Leather gloves-shoes
Navy jacket / Cognac gloves-shoes
Brown jacket / Burgundy gloves-shoes
Cloud-white jacket / Slate gloves-shoes
Blue jacket / Brown-leather gloves-shoes
```

---

## Appendix C — Standard ten design themes used during testing

These are design themes, not hardcoded index maps:

```text
1  Black / Crimson / contrasting leather / Oxblood
2  Black / Navy / Cognac or other separated tertiary / Blue-black
3  Emerald / Brown / Burgundy or separated warm tertiary / Warm brown
4  Sky blue / Cloud white / Slate or pale contrasting tertiary / Tan
5  Cream / Black / Warm taupe-brown / Dark brown
6  Black / Charcoal / Gold / Antique gold
7  Orange / Blue / Brown-leather tertiary / Dark brown
8  Purple / Black / White / Charcoal-violet
9  Charcoal / Dark charcoal / Medium charcoal / Near-black
10 Red / Crimson / Gold / Dark chestnut
```

Interpret each line as:

```text
Primary / Secondary / Tertiary / Quaternary
```

The exact color choices may be adjusted when a sprite's semantic regions require stronger separation or a shared-index compromise.

---

# Part VII — Production and Iteration

## 25. Production-generation principles

When building final palettes:

1. Start from a known-good matching `.pal`.
2. Preserve all untouched bytes.
3. Preserve fourth bytes.
4. Recolor only indices justified by the current mapping.
5. Generate coherent ramps rather than flat colors.
6. Preserve enough value range for pixel-art shading.
7. Keep semantic families visually distinct unless intentionally monochrome.
8. Use bridge colors for shared indices.
9. Preserve unresolved indices until mapped.
10. Test all eight directions before calling the palette production-ready.

---

## 26. Defect-driven refinement procedure

When a visual problem appears in-game:

```text
1. Identify exact visible defect.
2. Find the corresponding SPR frame/action/direction.
3. Inspect the pixel coordinates in the decoded frame.
4. Read the palette index at those pixels.
5. Determine whether that index is:
   - dedicated to the affected region,
   - part of a semantic ramp,
   - or shared with another region.
6. Adjust the mapping or color rule accordingly.
7. Regenerate and retest.
```

This is preferable to guessing based only on palette ranges.

Examples from the project:

```text
white Thief jacket speckles
→ traced to index 40
→ shared undershirt/jacket role
→ solved with tinted bridge

blue Thief boot patch
→ traced to index 73
→ not actually tied to jacket
→ moved to footwear-derived family
```

---

## 27. Cache strategy for future jobs

The project should gradually accumulate a mapping library keyed by exact sprite hash.

Conceptual structure:

```text
mappings/
  <spr_sha256>.yaml
  <spr_sha256>.md
```

Each entry should store:

```text
sprite identity
ACT identity
known-good PAL identity
used indices
structural statistics
semantic groups
shared indices
confidence per group/index
production notes
visual-test notes
```

Workflow for a future agent:

```text
hash sprite
↓
known hash?
  yes → load cached mapping
  no  → run generalized analysis
↓
review / validate
↓
generate palette
```

This minimizes repeated manual work without pretending that one fixed table applies globally.

---

## 28. Core principle

> **Parse first, understand the artwork second, assign semantic families third, design colors fourth.**

The SPR and ACT provide structural truth. Semantic grouping requires judgment. Good palette generation then requires color theory, material logic, readable value ramps, and explicit handling of shared indices.

The direct Acolyte and Thief mappings are retained because they are valuable validated examples and reusable cached outputs. The long-term system, however, should be driven by the generalized decoding and interpretation procedure described above.
