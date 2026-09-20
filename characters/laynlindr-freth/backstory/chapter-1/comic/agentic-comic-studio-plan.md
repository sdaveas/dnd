# Agentic Comic Studio — Production Plan

## Goal

Build an agentic comics-production pipeline that behaves like a small comics studio, with **fast targeted iteration**.

Core invariant:

> Change the smallest artifact that satisfies the request.

A request such as `Page 3 / Panel 2: make the background darker` should regenerate only that panel, re-render only page 3, and update the PDF. The PDF is an output artifact, never the source of truth.

---

## 1. Architecture

```text
                           USER
                            |
                            v
                  +--------------------+
                  | ORCHESTRATOR AGENT |
                  |   Project Manager  |
                  +---------+----------+
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
 +-----------+       +-------------+       +-------------+
 |   SCRIPT  |       | CHARACTER / |       |    ART      |
 |   AGENT   |       | CONTINUITY  |       |    AGENT    |
 +-----------+       +-------------+       +-------------+
       |                    |                    |
       +--------------------+--------------------+
                            |
                            v
                    +---------------+
                    | LAYOUT AGENT  |
                    +-------+-------+
                            |
                            v
                   +-----------------+
                   | LETTERING AGENT |
                   +--------+--------+
                            |
                            v
                 +---------------------+
                 | DETERMINISTIC       |
                 | PAGE RENDERER       |
                 +----------+----------+
                            |
                    +-------+-------+
                    |               |
                    v               v
                 PNG pages       comic.pdf
```

Separate the system into two worlds:

**Creative / expensive / nondeterministic:** LLMs, story adaptation, character generation, image generation, WildComiks MCP.

**Production / cheap / deterministic:** JSON/YAML, existing images, layout, fonts, SVG/HTML/CSS or Cairo/Pango, page rendering, PDF assembly.

This separation is what makes long-form comic iteration practical.

---

## 2. WildComiks Integration

Use WildComiks as the comic-aware generation service.

Current documented MCP tools:

- `parse_story` — optional prose-to-comic assistance
- `lock_character` — canonical recurring-character references
- `generate_panel` — individual panel generation
- `build_page` — optional comic-native page preview/layout
- `animate_panel` — future motion-comic phase

MCP reference: https://www.wildcomiks.com/mcp

WildComiks must **not** become the canonical project database. The project’s own structured files remain authoritative. `build_page` may be used for previews, while the deterministic renderer controls final exact page geometry, lettering, and human edits.

---

## 3. Agents

### 3.1 Orchestrator Agent / Project Manager

Responsibilities:

- interpret user requests
- inspect project state
- resolve page/panel IDs
- calculate affected dependencies
- delegate work
- track versions
- prevent unnecessary regeneration
- trigger rendering
- run QA
- report changed artifacts

It should not normally generate art or manipulate pixels directly.

Example:

```text
User: page 3, panel 2: make the lighting darker
        |
        v
resolve p003/panel-02
        |
        v
Art Agent -> new panel image
        |
        v
Renderer -> page-003.png
        |
        v
PDF update
```

### 3.2 Script Agent

Input:

- chapter/book/story material
- story notes
- existing comic script
- continuity information
- style guidance

Output:

```text
script/pages/page-001.json
script/pages/page-002.json
...
```

Each page/panel describes:

- camera/composition
- action
- characters
- location
- narration
- dialogue
- SFX
- image prompt
- layout requirements

The script describes **what the comic needs**, not implementation details of the renderer.

### 3.3 Character / Continuity Agent

Maintains canonical character definitions and references.

Example:

```yaml
id: laynlindr-freth-child
name: Laynlindr Freth
appearance:
  species: drow
  age_stage: child
  skin: dark charcoal-black
  hair: white
  eyes: red
  build: slender
  clothing: young noble drow clothing
visual_behavior:
  posture: quiet
  expression: restrained
  personality_visual: observant
negative_constraints:
  - no surface-elf appearance
  - no human appearance
  - no modern clothing
  - no adult proportions
```

Generate a canonical reference once and register it with WildComiks `lock_character`. Later panels reference the canonical definition.

### 3.4 Art / Image Agent

Preferred unit:

> one panel = one independently addressable artwork asset

Example:

```text
assets/panels/
  p001/panel-01/master.png
  p002/panel-01/master.png
  p002/panel-02/master.png
```

Store generation metadata:

```json
{
  "panel_id": "p002-panel-02",
  "generator": "wildcomiks",
  "generation_id": "...",
  "prompt": "...",
  "characters": ["laynlindr-freth-child"],
  "style_version": "style-v3",
  "version": 4
}
```

Prefer editing/inpainting of an existing panel when supported. Otherwise regenerate the single panel using the same references/style.

### 3.5 Layout Agent

Owns page geometry:

```json
{
  "page_id": "p003",
  "canvas": {"width": 2550, "height": 3300},
  "panels": [
    {"panel_id": "p003-panel-01", "rect": [0, 0, 2550, 1200]},
    {"panel_id": "p003-panel-02", "rect": [0, 1200, 1275, 2100]}
  ]
}
```

Also controls crop, focal point, gutters, borders, narration boxes, dialogue balloons, tails, and text placement.

### 3.6 Typography / Lettering Agent

Defines the comic's text language. Example:

```yaml
narration:
  font: "Cormorant Garamond"
  size: 14
  weight: regular
dialogue:
  font: "Comic Neue"
  size: 13
  weight: bold
sfx:
  font: "Bangers"
  size: 18
  weight: bold
```

Typography changes invalidate rendering only. They must never invalidate image generation.

### 3.7 QA Agent

Checks scripts, art, layout, continuity, fonts, clipping, missing assets, page count, and PDF integrity. QA reports errors rather than silently making creative decisions.

---

## 4. Canonical Project Structure

```text
comic/
├── source/
│   ├── chapters/
│   └── notes/
├── script/
│   ├── pages/
│   └── characters/
├── style/
│   ├── visual.yaml
│   ├── typography.yaml
│   └── references/
├── assets/
│   ├── characters/
│   ├── locations/
│   └── panels/
├── layout/
│   ├── pages/
│   └── templates/
├── render/
│   ├── pages/
│   └── pdf/
├── manifests/
│   ├── project.json
│   └── dependency-graph.json
└── README.md
```

For the current repo, the comic studio planning document lives under `characters/laynlindr-freth/backstory/chapter-1/comic/`.

---

## 5. Page Data Model

Every page must be reproducible from structured data.

```json
{
  "page_id": "p001",
  "title": "No Sky",
  "canvas": {"width": 2550, "height": 3300},
  "panels": [
    {
      "panel_id": "p001-panel-01",
      "type": "splash",
      "image": "assets/panels/p001/panel-01/master.png",
      "crop": {"x": 0.0, "y": 0.0, "scale": 1.0},
      "narration": [
        {"id": "n001", "text": "There was no sky above Menzoberranzan.", "rect": [100, 150, 700, 180]},
        {"id": "n002", "text": "There had never been one.", "rect": [100, 370, 650, 180]}
      ],
      "dialogue": [],
      "sfx": []
    }
  ]
}
```

Every visual element gets an addressable ID so targeted updates are possible.

---

## 6. Deterministic Renderer

The renderer is a normal program, not an LLM agent.

Preferred pipeline:

```text
JSON layout + panel images + fonts + style
                    |
                    v
              SVG / HTML / CSS
                    |
                    v
                 page PNG
                    |
                    v
                   PDF
```

SVG/HTML is attractive because coordinates, typography, boxes, balloons, and editing are deterministic and human-readable. Pillow/Cairo/Pango are valid alternatives.

Normal page render target: roughly seconds or less.

---

## 7. Human Editing

This is a first-class requirement.

A page editor should allow direct manipulation of:

- panel edges and positions
- image crop
- narration boxes
- dialogue balloons
- balloon tails
- text
- font
- font size
- balloon shape

The editor modifies layout/data directly and re-renders locally.

```text
layout.json
    |
    v
renderer
    |
    v
page.png
```

No LLM and no image generation for normal layout edits. Target interactive render latency: `< 1 second` where practical.

---

## 8. Dependency Graph

Every artifact declares dependencies.

```yaml
artifact: page-003
depends_on:
  - panel-003-01
  - panel-003-02
  - panel-003-03
  - layout-page-003
  - typography-v2
```

Example panel:

```yaml
artifact: panel-003-02
depends_on:
  - script-page-003-panel-02
  - character-laynlindr-v4
  - style-v3
```

The orchestrator traverses this graph to calculate the minimum invalidation set.

---

## 9. Update Matrix

| User change | Image generation | Re-render | PDF |
|---|---|---|---|
| Move narration box | No | One page | Update |
| Change narration text | No | One page | Update |
| Resize panel | No | One page | Update |
| Change crop | No | One page | Update |
| Change font | No | Affected pages | Update |
| Change one panel image | One panel | One page | Update |
| Change character design | Affected panels | Affected pages | Update |
| Change global visual style | Potentially all panels | All affected pages | Update |

Global changes should be treated as expensive and require explicit confirmation.

---

## 10. Fast Update Algorithm

For every request:

```text
1. Parse request.
2. Resolve artifact IDs.
3. Determine what changed.
4. Traverse dependency graph.
5. Compute minimal invalidation set.
6. Ask only required agents to work.
7. Regenerate only required creative assets.
8. Deterministically render affected pages.
9. Update PDF.
10. Run QA on affected outputs.
11. Report changed artifacts.
```

Example:

```text
p003/panel-02
      |
      v
image asset
      |
      v
p003
      |
      v
comic.pdf
```

No other page is touched.

---

## 11. PDF Strategy

Keep pages independently rendered:

```text
render/pages/001.png
render/pages/002.png
render/pages/003.png
...
```

Then assemble `comic.pdf`.

A full PDF assembly from already-rendered page PNGs should be cheap. Later, incremental PDF replacement can be added if useful, but PDF assembly must never be the expensive part of an image update.

---

## 12. Versioning

Use Git for canonical project state.

Version:

- scripts
- character definitions
- visual/typography styles
- layout files
- final panel masters
- generation metadata
- renderer code

Avoid committing unnecessary temporary intermediates.

Every generated asset should record generator, generation ID, prompt, references, style version, timestamp, and asset version.

---

## 13. Example Production Run

Input: `Chapter 1`

```text
Script Agent
  -> comic script
  -> pages
  -> panels

Character Agent
  -> canonical references

Art Agent
  -> WildComiks generate_panel
  -> panel images

Typography Agent
  -> fonts / sizes / balloon language

Layout Agent
  -> page geometry

Renderer
  -> PNG pages

PDF Builder
  -> comic.pdf

QA Agent
  -> validation
```

---

## 14. Example Targeted Updates

### Image change

```text
Page 3 panel 2: make the priestess more intimidating.

Orchestrator
 -> Art Agent
 -> WildComiks
 -> panel-003-02.png
 -> Renderer
 -> page-003.png
 -> PDF
```

No other image is generated.

### Layout change

```text
Move the narration box 40 pixels down.

Orchestrator
 -> layout/page-003.json
 -> Renderer
 -> page-003.png
 -> PDF
```

Zero image generation.

### Character change

```text
Make young Layn's hair longer.

Character Agent
 -> canonical reference
 -> find dependent panels
 -> regenerate affected panels
 -> render affected pages
 -> PDF
```

The orchestrator should show the scope before an expensive fan-out.

---

## 15. Agent Communication Contract

Agents exchange structured artifacts rather than long natural-language conversations.

Example request:

```json
{
  "task_id": "task-2026-00123",
  "operation": "regenerate_panel",
  "panel_id": "p003-panel-02",
  "reason": "user_requested_lighting_change",
  "inputs": {
    "script_version": "v12",
    "character_versions": {"laynlindr-freth-child": "v4"},
    "style_version": "v3",
    "previous_asset": "assets/panels/p003/panel-02/master.png"
  }
}
```

Result:

```json
{
  "status": "completed",
  "panel_id": "p003-panel-02",
  "asset": "assets/panels/p003/panel-02/master-v5.png",
  "generation_id": "..."
}
```

---

## 16. Human Approval Boundaries

Require approval before expensive operations:

- regenerate an entire chapter
- change global visual style
- change canonical character appearance
- replace many panels
- spend a large image-generation budget

Do not require approval for cheap deterministic operations:

- move a box
- resize a panel
- change text
- change crop
- render a page
- rebuild the PDF

---

## 17. MVP Roadmap

### MVP 1

```text
comic script JSON
   -> panel images
   -> layout JSON
   -> SVG renderer
   -> PDF
```

Use one page.

### MVP 2

Add:

- WildComiks MCP
- character references
- style guide

### MVP 3

Add a visual page editor for drag/drop panels and text.

### MVP 4

Add:

- dependency graph
- incremental rebuilds
- QA agent

### MVP 5

Add:

- batch generation
- continuity checking
- version comparison

---

## 18. First Test Case — Layn Page 1

Use the existing comic script:

```text
I.1 — Beneath the Spider's City
Page 1 — No Sky
```

It is a full-page splash with:

- extreme-wide Menzoberranzan cavern
- enormous towers
- immense rock formations
- stalactites disappearing into darkness
- huge bridges
- tiny magical lights
- individual drow almost impossible to distinguish
- narration:
  - `There was no sky above Menzoberranzan.`
  - `There had never been one.`

Generate the artwork through WildComiks, but compose the narration independently through the deterministic renderer.

**Do not bake narration/dialogue into generated artwork.**

---

## 19. Definition of Done

The architecture is correct when:

### Layout-only change

User:

> Page 7, panel 3: move the narration box down 40px.

System:

```text
modify layout
 -> render page 7
 -> update PDF
```

No image generation.

### Image-only change

User:

> Page 7, panel 3: regenerate the image with a darker background.

System:

```text
Art Agent
 -> WildComiks
 -> new panel
 -> render page 7
 -> update PDF
```

No other panels regenerate.

### Typography-only change

User:

> Change narration font from 14px to 13px.

System:

```text
Typography config
 -> render affected pages
 -> update PDF
```

No image generation.

---

## 20. Key Invariant

The entire system should preserve:

> **Change the smallest artifact that satisfies the request.**

Creative generation is expensive and nondeterministic.

Rendering is cheap and deterministic.

Therefore:

```text
creative change
    -> regenerate minimum creative asset
    -> deterministic render
```

and:

```text
layout/text change
    -> deterministic render only
```

That is the architecture that makes a long comic practical to iterate on.
