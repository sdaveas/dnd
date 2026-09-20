# Batch Manifests

Batch manifests are the shared way to aggregate sections or chapters for the writing, audiobook, and comics teams.

## File convention

Create one YAML file per batch under `labs/batches/`, using a stable name such as `chapter-1.yml` or `part-i.yml`. Start from [`template.yml`](template.yml).

The manifest must define:

- a stable `batch_id` and human-readable title;
- the ordered chapters and sections in scope;
- the path to each artifact that exists or is expected;
- the work requested from each team;
- the batch status and any known gaps.

## Processing rules

1. Read the manifest before starting batch work.
2. Process each listed section independently, in manifest order unless parallel work is explicitly requested.
3. Use the writing artifact as the continuity anchor; audiobook and comics adapt from its approved revision.
4. Aggregate only after section-level work is complete or explicitly marked incomplete.
5. Preserve the manifest order and label every aggregate item with its chapter and section ID.
6. Report missing or stale artifacts instead of silently omitting them.

The manifest is coordination metadata. It should point to canonical files, not contain a second copy of the novel, script, or audio.
