# Shared Production Rules

These rules apply to every writing, audiobook, and comics agent.

## Authority

1. The current character files and approved manuscript are the active project state.
2. `characters/laynlindr-freth/backstory/notes.md` is the source of truth for story decisions, canon constraints, and unresolved questions.
3. [`Forgotten Realms Wiki`](https://forgottenrealms.fandom.com/) is the default research index for Forgotten Realms names, places, houses, relationships, chronology, and setting details.
4. Files under `source/` are references, not automatically approved story text.
5. Published Forgotten Realms canon and the project's explicit decisions outrank an agent's invention.

When sources conflict, stop and identify the conflict. Do not silently choose a version or erase a user's existing work.

## Canon research protocol

- Before inventing a named character, house, place, historical event, or relationship, search the Forgotten Realms Wiki first.
- Prefer an existing canonical name or detail when it fits the time period and location. Invent only what the sources leave open or what the project explicitly marks as **OUR STORY**.
- Follow the wiki page's cited primary sources when a detail materially affects chronology, survival, family relationships, or published events.
- Treat the wiki as a secondary compiled reference: it can contain omissions, editorial notes, source conflicts, and assumptions. Record uncertainty instead of presenting a disputed detail as fact.
- Keep a clean boundary between **CANON**, **OUR STORY**, and **UNKNOWN** in notes and planning files.
- When using a wiki fact in a draft, preserve the page URL in the relevant planning note or research record so another team can verify it.

## Collaboration

- Read the relevant lab guide before editing.
- Inspect the current file and nearby files first.
- Preserve user changes and keep edits scoped to the request.
- Do not commit, push, or publish unless explicitly asked.
- Use descriptive, stable filenames and keep related outputs beside their source artifact.
- Do not create duplicate “final”, “new”, “latest”, or timestamped copies. Replace the approved artifact or use a clearly named archive only when the user asks for version history.
- Update the table of contents or artifact README when a move changes discoverability.

## Section-level isolation

Every team must be able to work on one story section without loading or changing the whole book.

- Treat a section as the smallest independent production unit: its approved novel markdown, its audio render, and its comic script belong to the same section packet.
- Start with the target section, `notes.md`, and the TOC. Read adjacent sections only when continuity requires it.
- Do not rewrite, re-render, or re-panel neighboring sections unless the user explicitly asks for a cross-section change.
- Keep section outputs in the matching chapter and format directories. Use the same section identity in filenames so prose, audio, and comics can be paired reliably.
- A team handoff should name the exact section, source revision, current status, and any unresolved continuity issue.
- If a section depends on a fact from elsewhere, record the dependency briefly in the section handoff or notes rather than copying the other section's content.

The default unit of work is therefore **one section in, one section out**. Chapter-wide or book-wide passes are explicit exceptions.

## Batch aggregation

Batch work uses one shared manifest for every team. Manifests live under `labs/batches/` and use the `.yml` extension.

- The manifest is the single definition of scope and order for a batch of sections or chapters.
- It lists each chapter and section once, with its novel, audio, and comic paths when those artifacts exist.
- Writing, audiobook, and comics agents read the same manifest but process each listed section as an isolated unit.
- Aggregation means producing a batch-level sequence or report from the listed artifacts; it does not mean merging source files or weakening section boundaries.
- Missing artifacts are reported as `planned`, `in-progress`, or `missing`; agents do not silently skip them.
- A batch output must preserve the manifest order and identify the source section for every item.
- If the scope changes, update the manifest before editing or rendering so all teams work from the same batch definition.

## Quality gate

Before handing off work, verify:

- the edited files are in the intended directory;
- links and references use current paths;
- no section was truncated or duplicated;
- the result follows the specialist guide;
- `git diff --check` passes when text files changed.

If a decision is unresolved, record it in `notes.md` or report it to the user rather than burying it in prose, audio, or panels.
