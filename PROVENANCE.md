# Provenance and Attribution

This file records authorship and contribution split for the Sambar deer
graduation project so reviewers can verify the work history.

## Project context

The project began as a 5-person undergraduate group graduation project in
the 2023–2024 academic year (大三上_逢甲, original development location:
`C:\Users\skybl\Desktop\大三上_逢甲\進階專題\` — visible in the legacy
notebooks' file paths and original output logs as supporting evidence).

It has continued as solo development work after the group submission.

## Contribution split

### Group project phase (2023 — 2024)

**Code, algorithm design, system implementation, and the project
presentation: this repo's owner.**

- All deer-detection / motion-classification algorithm work
- Live camera program (`capture_process.py`) — tkinter UI, threaded
  capture/processing pipeline, ROI selection, LINE alert integration
- All five experimental notebooks (`Basic`, `Test1`, `Final1`, `Final2`,
  `MakeDF`) — feature engineering, the failed LSTM attempts and pivot to
  threshold-based classification, K-means validation, Gaussian-threshold
  experiment, end-to-end pipeline
- Delivered the in-class project presentation

Approximate share of code/algorithm work: **99%**.

**Other 4 group members:** prepared the PowerPoint slide deck for the
in-class presentation.

The group also collaboratively co-authored the original project proposal
document (`docs/水鹿計畫書.pdf`).

### Solo continuation phase (post-submission, 2026 —)

Work done independently after the group project was submitted, all in
`solo_v2/`:

- Consolidated the five experimental notebooks (`Basic`, `Test1`,
  `Final1`, `Final2`, `MakeDF`) into a single research-journey notebook
  (`solo_v2/notebooks/00_research_journey.ipynb`) that traces the
  research path end-to-end with cleaned-up code, relative paths, and a
  reflection block at each pivot
- Refactored the live program to load the LINE Notify access token from
  a `.env` file via `python-dotenv` instead of hardcoding it — security
  improvement after the group project closed
- Reorganised the repository into `legacy_v1_group/` (frozen group
  deliverable) and `solo_v2/` (active solo work) structure
- Wrote project-level documentation (this file, the top-level README,
  per-folder READMEs)

Planned (not yet implemented):
- Held-out evaluation: re-calibrate thresholds on a subset of clips and
  report a confusion matrix on the held-out remainder, instead of
  validating on the same data used for calibration
- Sensitivity analysis on the 25/75 percentile thresholds
- Optional pre-filter: add a pretrained YOLO deer-presence gate so the
  alarm only fires on actual deer motion, not wind or other animals

## Verification points

- The five legacy notebooks at `legacy_v1_group/notebooks/` retain their
  original execution outputs (LSTM accuracy logs, dataframe printouts,
  cluster assignments, "處理影片：..." print statements showing the
  original Desktop development paths).
- File modification timestamps on the legacy notebooks date from
  2023-12 to 2024-05.
- Git history (once initialised) will show the solo continuation commits
  authored by the repo owner only.
- The early draft `legacy_v1_group/early_drafts/Test1_2024-01-05.ipynb`
  is dated 2024-01-05 — the earliest preserved code artifact, also from
  the repo owner.
