# Legacy — group project deliverable (2023 – 2024)

Frozen snapshot of the group graduation project as it existed at the time
of submission. Nothing in this folder should be edited; new work happens
in `../solo_v2/`.

The five experimental notebooks here represent the research path the
group project took:

| File | What it does | Key result |
|---|---|---|
| `notebooks/Basic.ipynb` | First OpenCV motion-detection prototype on a webcam (running-average background subtraction + contours + bounding boxes) | Working live demo |
| `notebooks/Test1.ipynb` | Same algorithm applied to multiple recorded deer videos | Confirms the pixel-difference signal works on real footage |
| `notebooks/Final1.ipynb` | Refines `Basic` to *quantify* activity per frame (count nonzero pixels) and emit a per-frame DataFrame | Total activity 48,629,694 on `水鹿1.mp4`; 599 frames |
| `notebooks/MakeDF.ipynb` | Builds the labelled dataset across N/A/P clips, then tries an LSTM at three different time granularities | LSTM plateaus at ~50–58% accuracy (per-frame); drops to 31% per-second |
| `notebooks/Final2.ipynb` | Pivot — abandons the LSTM, switches to percentile-threshold classification on relative pixel diffs; adds K-means validation; tries Gaussian thresholds (fails); ends with the calibrated thresholds the live program uses | 受水驚嚇 → 87% Aggressive ✓ |

These notebooks all contain the original execution outputs (training
logs, dataframe printouts, cluster assignments). They reference video
paths under `C:\Users\skybl\Desktop\大三上_逢甲\進階專題\...` from the
original development machine — those paths no longer exist, so the
notebooks are not runnable as-is, but every output cell is preserved
exactly as it ran during the group-project phase.

## Live program

`live_program/capture_process.py` is the camera-feed program as
submitted. It opens a tkinter window, lets the user drag a region of
interest, classifies motion inside the ROI as `Aggressive` / `Normal` /
`Passive`, and on `Aggressive` sends a LINE Notify message.

The hardcoded LINE Notify access token that was in the file at submission
has been **redacted to a placeholder string** for security — see the
docstring at the top of the file. The token itself was invalidated when
LINE Notify was discontinued by LINE on 2025-03-31.

`live_program/capture_process_no-line.py` is an even earlier draft from
mid-May 2024, before the LINE alert step was added. Same algorithm,
fewer lines.

## Early drafts

`early_drafts/Test1_2024-01-05.ipynb` is the earliest preserved code
artifact (5.7 MB — the size is from cached cell outputs / images). It
predates the rest of the notebooks and is mostly experimentation; kept
for the timestamp.

## See also

- `../PROVENANCE.md` for the contribution attribution
- `../solo_v2/` for the consolidated narrative + solo follow-on work
