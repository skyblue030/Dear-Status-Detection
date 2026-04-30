# Paths

The active notebook in this directory is `00_research_journey.ipynb`. It uses
the following paths, relative to this directory:

- Labeled clips:  `../../data/labeled/`
- Raw videos:     `../../data/raw/水鹿影片/`
- N/A/P clips:    `../../data/raw/水鹿影片/水路剪輯/{N,A,P}/`
- Tables I/O:     `../../data/tables/`
- Trained model:  `../../models/best_decision_tree_model.pkl`

Constants are defined in the Setup cell (`DATA_LABELED`, `DATA_RAW_VIDEO`,
`DATA_TABLES`, `STATUS_FOLDERS`).

## Legacy notebooks

The five notebooks that this one consolidates are in
`../../legacy_v1_group/notebooks/`:

- `Basic.ipynb`   — initial OpenCV motion detection PoC on webcam
- `Test1.ipynb`   — applying the algorithm to multiple deer videos
- `Final1.ipynb`  — quantifying activity on a single recorded video
- `MakeDF.ipynb`  — building the labelled dataset + LSTM attempts
- `Final2.ipynb`  — threshold-based pipeline + K-means + Gaussian experiment

They contain hardcoded absolute paths from earlier development locations
(`C:\Users\skybl\Desktop\大三上_逢甲\...`) and won't run as-is, but their
execution outputs (LSTM accuracies, dataframes, cluster assignments) are
preserved if you ever need to look back at the original results.
