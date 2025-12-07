# Feature Request Analysis and Processing: Tasks, Techniques, and Trends — Snowballing Scripts

This folder contains the helper scripts used in the paper **"Feature Request Analysis and Processing: Tasks, Techniques, and Trends"** for collecting and expanding the paper dataset.

## Files

- `getDoi.py`: Reads an Excel file `ForSnowballing.xlsx` (must contain at least `Title` and `Publication Year` columns), queries the Semantic Scholar API, and outputs `papers_with_ids.xlsx` with DOI and Semantic Scholar `PaperId` for each paper.
- `snowballing.py`: Takes `papers_with_ids.xlsx` as input, performs one round of forward and backward snowballing using Semantic Scholar (based on `PaperId`), and writes the discovered papers and basic metadata to `snowball_output.xlsx`.

These scripts are intended as simple, task-specific utilities and are **not** a general-purpose library. Adjust the configuration constants at the top of each script (e.g., input/output file names) as needed for your own replication or experiments.
