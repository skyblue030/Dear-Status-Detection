# Solo continuation (post-submission, 2026 —)

Work done independently after the group graduation project closed.

## What's new since `../legacy_v1_group/`

- **`notebooks/00_research_journey.ipynb`** — single consolidated
  notebook that traces the entire research path from the legacy phase:
  initial PoC → quantification → labelled dataset → LSTM failures →
  pivot to threshold-based classification → K-means sanity check →
  Gaussian-threshold failure mode → final tuned pipeline → live
  deployment pointer. Each pivot has a *Reflection* markdown block
  explaining what was learned.
  - Cleaned code from the five legacy notebooks; all paths converted
    to relative
  - Verbose epoch-by-epoch training logs trimmed; key results inlined
    as comments
  - Reads top-to-bottom as a thesis-style writeup

- **`live_program/capture_process.py`** — same algorithm as the legacy
  version, but with two security improvements:
  - LINE Notify access token now read from `.env` via `python-dotenv`
    instead of hardcoded as a string literal
  - `.env` is gitignored; `.env.example` at the repo root documents the
    expected variable name

- **`evaluation/`** — empty placeholder for the next planned solo work
  (held-out evaluation + sensitivity analysis on the 25/75 thresholds;
  see `../PROVENANCE.md` for the roadmap).

## How to read this

Open `notebooks/00_research_journey.ipynb`. It's structured as a
narrative — section headers describe each step of the research path,
markdown cells between code blocks explain the why, and inlined
comments record the actual results from the original group-project
runs (since the venv that produced those results is no longer
functional).

## Path conventions

The notebook references the shared video corpus and tables via paths
relative to its own location:

- `../../data/labeled/` → 24 behaviour-tagged clips (gitignored)
- `../../data/raw/水鹿影片/` → raw deer videos (gitignored)
- `../../data/raw/水鹿影片/水路剪輯/{N,A,P}/` → labelled split
- `../../data/tables/` → xlsx datasets and pipeline outputs (in git)
- `../../models/` → trained-model artefacts

See `notebooks/PATHS.md` for the legacy-notebook recovery checklist if
you ever need to revive one of the originals.
