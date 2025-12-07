# Feature Request Survey

This repository accompanies the paper **"Feature Request Analysis and Processing: Tasks, Techniques, and Trends"**. It contains scripts and artifacts used to collect, process, and analyze feature request–related data.

## Structure

- `Snowballing/`: Helper scripts for building the literature dataset via Semantic Scholar.
  - `getDoi.py`: Given `ForSnowballing.xlsx` (with at least `Title` and `Publication Year` columns), queries the Semantic Scholar API and produces `papers_with_ids.xlsx` with DOI and Semantic Scholar `PaperId`.
  - `snowballing.py`: Uses `papers_with_ids.xlsx` as seed papers and performs one round of forward and backward snowballing, outputting `snowball_output.xlsx`.

These materials are intended to support replication of the study and to illustrate the data collection workflow, rather than to serve as a polished, general-purpose toolkit.
