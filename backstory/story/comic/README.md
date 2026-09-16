# Layn Comic

The comic adaptation is kept separate from the prose story.

## Structure

- `style.md` — global visual and storytelling language for the comic.
- `part-i/` — comic scripts for individual story sections.
- Future `art/` or `prompts/` directories may contain image-generation prompts and production assets; these should remain separate from the script.

## Separation of Concerns

### Story prose

`backstory/story/part-i/...`

Defines the actual narrative: scenes, prose, dialogue, events, characterization, and story progression.

### Comic script

`backstory/story/comic/part-i/...`

Defines how the narrative is translated into sequential art:

- Page
- Panel
- Panel layout
- Camera/composition
- What is visible
- Narration
- Dialogue
- Sound effects
- Story purpose
- Continuity requirements

The comic script should not contain the global visual style. It references `backstory/story/comic/style.md` instead.

### Art prompts

Future image-generation prompts should be separate from both the story and the comic script. They translate an approved panel into instructions for an image model while inheriting the global style and continuity rules.

## Workflow

1. Lock the story section.
2. Build the comic page/panel script.
3. Review pacing and visual storytelling.
4. Lock visual continuity.
5. Generate art prompts.
6. Generate artwork.
7. Review continuity and revise.
