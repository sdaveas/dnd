# Audiobook Team Skill

## Scope

This guide applies to voice rendering and audio QA for the approved novel sections.

## Source and delivery

- Render only from the current approved markdown, never from an old draft, review copy, or an audio file.
- Use Sonia as the approved voice unless the user explicitly chooses another voice.
- Keep the render beside its source section in `chapter-*/novel/audio/`.
- Use a stable descriptive filename such as `section-2-web-of-lolth-sonia.mp3`.
- MP3 is the standard delivery format. Produce another format only when requested or when it materially improves compatibility.
- Render a complete section by default. Excerpts are samples only and must be clearly labeled when explicitly requested.

## Reading style

- Preserve paragraph breaks and the natural pacing of the prose.
- Keep narration distinct from dialogue through phrasing and pauses, not by inventing dialogue tags.
- Do not read markdown headings, file paths, production notes, or drafting comments unless the user asks for them.
- Correct obvious text-to-speech pronunciation issues through a pronunciation guide or rendering preparation, not by changing the manuscript silently.
- Preserve names and terms consistently: Laynlindr, Layn, Freth, Menzoberranzan, Lolth, Teken'Duis, and Melee-Magthere.

## QA checklist

Before delivery:

- confirm the audio covers the entire approved section;
- check that it does not end at a scene boundary by mistake;
- listen to the opening, middle, and ending for clipping, silence, truncation, and pronunciation;
- compare the render against the current markdown after any prose edit;
- keep only the current requested render in the active audio directory.

Do not keep old renders, test files, or duplicate formats in the active directory. If version history is explicitly needed, ask where it should live before creating it.

## Batch mode

For a batch request, read the shared manifest under `labs/batches/`, render or collect only the listed approved sections, and preserve manifest order in any aggregate playlist or delivery report. A batch render must identify its chapter and section boundaries and must not replace the per-section audio files.
