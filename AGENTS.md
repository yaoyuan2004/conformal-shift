# Project agent instructions

## Keep only current files

- Keep one authoritative, latest version of each project file. Do not create or retain obsolete copies, backup files, or archive folders as a substitute for version history. Use Git for version management.
- Keep an archive only when it is still required by the current workflow or the user explicitly requests it. When replacing a file, update the authoritative copy rather than creating a dated or suffixed duplicate.
- Before deleting any local or Google Drive file or folder, have a separate `gpt-6.1-sol` agent with low reasoning effort review that exact deletion candidate for downstream code or runtime impact. Delete only after explicit approval; if approval is denied, preserve the item and report why.

## Notebooks and compute

- When updating a notebook, sync the current authoritative version to the project's Google Drive notebook folder.
- Prefer static inspection and existing outputs/caches. Do not execute GPU training, GPU preflight, or model-inference cells just to validate edits. Check whether a notebook can use existing cached results before running any expensive computation.
