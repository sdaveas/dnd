# Comics Team Skill

## Scope

This guide applies to comic scripts, visual continuity, page and panel plans, and future art prompts under `chapter-*/comic/`.

## Source and separation

- Start from approved novel prose. The writing team owns story facts; the comics team owns visual translation.
- Keep one section script per novel section where practical.
- Keep global visual rules in `style.md`, story-specific panel instructions in the section script, and image-generation prompts separate from both.
- Do not put prose drafts, audio instructions, or unrelated production notes into a panel script.

## Adaptation principles

- Preserve the scene's dramatic purpose, character motivation, continuity, and reveal order.
- Compression is allowed for pacing, but do not invent lore, change who knows what, or resolve an open story question.
- Every page and panel should have a clear purpose: establish, reveal, escalate, contrast, or transition.
- Narration should carry information that cannot be shown; dialogue should sound like something the character would actually say.
- Keep dialogue short enough to read comfortably in a panel and distinct enough to follow without the prose beside it.
- Mark visual continuity explicitly when it matters: age, clothing, hierarchy, architecture, lighting, injuries, props, and spatial position.

## Layn and Menzoberranzan anchors

- Menzoberranzan should feel enormous, vertical, carved from living stone, and shaped by darkness and magical light.
- Spiders in the city are architectural and religious imagery, not a swarm across ordinary streets.
- Show hierarchy through blocking and eye-lines: Layn is a young noble male, older noble males stand above him, and female authority dominates the house.
- Preserve the difference between the narrator's use of “Layn” and how characters address him in the scene.
- Do not turn drow cruelty into theatrical villain speeches. Let the panel composition, silence, gestures, and consequences carry the weight.
- Drow commerce is guarded and male-run: no open markets, no noble females shopping or bargaining. If a scene needs trade, depict a guarded exchange or depot run by male merchants; noble females appear only as distant, uninvolved authority (a passing priestess on ritual business, an idle watcher on a private gallery).

## Visual variety discipline

Similar-looking panels — especially on the same page — read as a broken comic. Before art prompts are written, every page's panel set must pass a variety check:

- **Camera-subject-lighting axis:** each panel is defined by (shot size, subject, light direction). No two panels on the same page may share more than one of the three. A page of four wide city vistas fails; a wide vista + macro carving + crowd + interior passes.
- **Shot size ladder:** each page should move through at least two different shot sizes (extreme-wide / wide / medium / close / extreme close-up). Establishing pages may lean wide, but never with identical subjects.
- **Anchor-and-rotate:** if a scene must stay in one location across several panels, rotate the axis instead of repeating it — same hall, different subject each time: architecture → object → face → eyes.
- **Contrast beat:** the final panel of a page should contrast the opening (scale, light, or intimacy), not echo it.
- Write the axis (shot size, subject, light) as a one-line matrix above the panel list in the section script, and verify it during the continuity pass. If two panels collide, revise the panel plan before writing prompts — narration can usually stay untouched because atmospheric lines survive scene changes.

## Handoff workflow

1. Confirm the prose section and its continuity notes.
2. Define the comic section's emotional arc and essential beats.
3. Break the beats into pages and panels with camera, action, narration, dialogue, and sound — run the visual variety matrix above.
4. Run a continuity pass against the prose and `style.md`, including the variety check.
5. Mark the script ready for art prompts only after the story team approves the adaptation.

## Batch mode

For a batch request, read the shared manifest under `labs/batches/`, process the listed comic sections independently, and aggregate scripts or page plans in manifest order. Do not merge section scripts into a new canonical source file unless the user explicitly requests a compiled production packet.
