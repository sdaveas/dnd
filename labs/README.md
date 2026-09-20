# Layn Production Lab

The lab contains the operating guides for the teams that develop Layn's backstory and its adaptations. It is a coordination layer, not story content.

All teams use the [Forgotten Realms Wiki](https://forgottenrealms.fandom.com/) as the default setting-research index, following the canon and uncertainty rules in [`shared/AGENTS.md`](shared/AGENTS.md).

## Team guides

- [`shared/AGENTS.md`](shared/AGENTS.md) — rules for every agent and artifact.
- [`writing/SKILL.md`](writing/SKILL.md) — novel prose, planning, continuity, and story decisions.
- [`audiobook/SKILL.md`](audiobook/SKILL.md) — Sonia renders, pronunciation, file naming, and audio QA.
- [`comics/SKILL.md`](comics/SKILL.md) — comic scripts, visual continuity, panel structure, and art handoff.
- [`batches/README.md`](batches/README.md) — the shared manifest format for aggregating sections and chapters.

## Routing

| Artifact | Guide |
| --- | --- |
| `characters/laynlindr-freth/backstory/*.md` | Writing |
| `characters/laynlindr-freth/backstory/chapter-*/novel/*.md` | Writing |
| `characters/laynlindr-freth/backstory/chapter-*/novel/audio/` | Audiobook |
| `characters/laynlindr-freth/backstory/chapter-*/comic/` | Comics |

When a task changes more than one artifact type, the writing guide remains the continuity anchor and the other teams adapt from its approved text.

For a batch task, every team uses the same manifest from [`batches/`](batches/). The manifest defines scope and order; it does not replace section-level isolation.

## Default production unit

Teams work section by section. For a target section, the writing team owns the approved prose, the audiobook team renders that prose, and the comics team adapts that same prose. A team should not need to process the rest of the chapter to complete a section-level task.
