# Retrace eLearning — Website Test Package

**Package type:** Standalone test assets and preview. **Not integrated into `base.zip`.**

## Contents
- `index.html` — responsive standalone preview of the approved seven-section eLearning page.
- `data/elearning_test_seed.json` — source-derived test curriculum and UI metadata.
- `assets/What Is Space Junk and Abandoned Space Hardware.pdf` — original supplied source PDF.
- `docs/SOURCE_AND_RECONCILIATION_NOTES.md` — source limitations and discrepancies.

## Run locally
For browsers that block `fetch()` from `file://`, run a local static server from this folder, for example `python -m http.server 8000`, then open `http://localhost:8000`.

## Important data integrity notice
The uploaded PDF is the source of the Chat 1 lesson records in this test seed. It contains nine lessons, with chapter counts 5, 5, 9, 11, 5, 5, 5, 5 and 5. Some chapter titles have no body text in the PDF. Those entries are retained as title-only; missing text has not been invented.

Earlier design context described Chat 1 as seven lessons with nine learning units each. That conflicts with this uploaded PDF. This package intentionally preserves the PDF structure and flags the conflict for approval before production use.

Chat 2 contains only previously supplied collection/subject metadata (3 subjects, 32 chapters). No Chat 2 chapter titles or content are fabricated.

Education level and difficulty are unclassified in the source. Filter controls are visible for UI testing, but should not be treated as validated classifications. The preview's notes, bookmarks, project save, export, quizzes and teacher-resource cards are demonstrations/placeholders; no backend persistence or downloadable resource content is connected.

All IDs with `TEST` are test identifiers, not production IDs. This content has not undergone NASA factual verification and is not publication-ready.
