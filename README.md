# Sambar Deer Activity Analysis

A computer-vision graduation project: detect *unusually active* Formosan
Sambar deer (`水鹿`) in camera-trap footage from Taiwan's alpine
ecosystems, and raise an alert when something out of the ordinary
happens.

This repository contains both the original group-project deliverable
(2023–2024) and continuing solo development work after submission.
**See [PROVENANCE.md](./PROVENANCE.md) for the contribution attribution.**

## Repo layout

| Folder | What's inside |
|---|---|
| **[`legacy_v1_group/`](./legacy_v1_group/)** | Frozen snapshot of the group-project deliverable as submitted. Five experimental notebooks (`Basic`, `Test1`, `Final1`, `Final2`, `MakeDF`) with their original execution outputs preserved, plus the live camera program. Don't edit; read-only history. |
| **[`solo_v2/`](./solo_v2/)** | Active solo continuation. The five legacy notebooks consolidated into a single research-journey notebook with cleaned-up code and reflections at each pivot. The same live program with security improvements (LINE token moved out of source into `.env`). Empty `evaluation/` placeholder for the next planned work. |
| `data/` | Shared video corpus and result tables. Videos are gitignored (~2.4 GB); `data/tables/` xlsx files are tracked. |
| `models/` | Trained-model artefacts. |
| `docs/` | Original project proposal (`水鹿計畫書.pdf`) and presentation materials (`簡報用素材/`). |

## Reading order for someone new

1. **[`PROVENANCE.md`](./PROVENANCE.md)** — who did what
2. **[`solo_v2/notebooks/00_research_journey.ipynb`](./solo_v2/notebooks/00_research_journey.ipynb)** — the full research story end to end, with code and reflections at each pivot
3. **[`legacy_v1_group/notebooks/`](./legacy_v1_group/notebooks/)** — the five original experimental notebooks with their actual execution outputs (LSTM accuracy logs, dataframe printouts, cluster assignments) for verification
4. **[`docs/水鹿計畫書.pdf`](./docs/)** — the original project proposal in Chinese

## What the project is, in 30 seconds

Wildlife researchers deploy camera traps in Sambar deer habitat. Most of
the recorded hours show resting or absent deer — only a small fraction
is interesting. The aim is to **flag the unusual**: clips with
abnormally high motion intensity that might indicate startle, fight, or
other behaviour worth a researcher's attention.

The system has two parts:

- **Live scope detection** (`*/live_program/capture_process.py`) — a
  tkinter+OpenCV program where the user drags a region of interest on
  a live camera feed; the program classifies motion inside the ROI
  every 5 seconds and pushes a LINE alert on `Aggressive`.
- **Deer classification** (`*/notebooks/`) — an offline pipeline that
  builds a per-frame motion-intensity dataset across labelled clips,
  calibrates classification thresholds at the 25th and 75th percentiles
  of the activity distribution, and validates with K-means clustering.

## Headline result

After trying and rejecting an LSTM-based classifier, the working
pipeline is **calibrated percentile thresholds** (no learning):

1. Run pixel-difference motion detection on all 24 labelled clips
   (~15 000 frames)
2. Take 25th and 75th percentiles as low/high thresholds
3. Each frame: `Aggressive` (above 75th), `Normal` (between), `Passive`
   (below 25th)
4. A clip whose frames are >75% one class gets that label; otherwise
   `Normal`

On the validation clip `受水驚嚇.mp4` (a deer startled by water — clearly
aggressive): **96% of frames classified as Aggressive** with the tuned
final thresholds; **87%** at the initial 30/70 calibration. Either way,
matches the human label.

| Clip | Aggressive % | Normal % | Passive % | Verdict |
|---|---:|---:|---:|---|
| `受水驚嚇.mp4` (startled by water) | 87 | 12 | 0 | **Aggressive** |
| `繞圈走動.mp4` (circling) | 87 | 12 | 1 | **Aggressive** |
| `走來走去.mp4` (pacing) | 69 | 26 | 6 | Normal (below 75% rule) |
| `休息2.mp4` (resting) | 3 | 18 | 79 | **Passive** |
| `走過來給鹿舔.mp4` (approaching) | 5 | 15 | 80 | **Passive** |
| `亂走亂舔.mp4` (wandering) | 4 | 24 | 72 | Normal |

The pipeline correctly separates startle / circling clips from resting
clips. Borderline cases fall back to `Normal` — desired conservative
behaviour: don't raise an alarm unless the signal is clearly abnormal.

## What didn't work, and why

Documented section by section in the journey notebook. Headlines:

- **LSTM on per-frame activity counts** — plateaued at 50–58% accuracy.
  A single scalar per "timestep" gives the LSTM nothing to model; the
  bottleneck was the feature, not the model.
- **Coarser per-second granularity** — dropped to 31% accuracy. Less
  data, no extra signal per row.
- **Gaussian-based thresholds (mean ± σ)** — erased the `Passive` class
  because the activity distribution is right-skewed.

The pivot from "train a classifier" to "calibrate thresholds against
the labelled distribution" was both simpler and more effective.

## Note on data

The video corpus (~2.4 GB) is gitignored — too large for GitHub and not
needed to read the notebook. The journey notebook's narrative cells and
inlined result comments are enough to follow the story without
re-executing anything.

## Setup notes

Python 3.10+, dependencies in `requirements.txt`. The original `dear/`
venv was built against a Python install that no longer exists on the
development machine, so it has to be recreated:

```bash
python -m venv dear
dear\Scripts\activate          # Windows
pip install -r requirements.txt
```

The live program reads its LINE token from `.env` (template at
`.env.example`). Note that LINE Notify itself was discontinued by LINE
on 2025-03-31, so the existing alert mechanism would need to be
replaced (LINE Messaging API, Discord webhook, or similar) to be
functional today.

Neither blocks the notebook from being *read*, which is the purpose of
this repo.
