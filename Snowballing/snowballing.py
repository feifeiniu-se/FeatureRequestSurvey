"""
Snowballing script: run 1 round of forward + backward discovery.
Input: Excel file with PaperId column (configurable below).
Output: Excel file with discovered papers (configurable below).
"""

import itertools
import os
import pickle
import time
from semanticscholar import SemanticScholar
import pandas as pd

# =============================================================================
# Configuration section - specify input/output files here
# =============================================================================
INPUT_FILE = "papers_with_ids.xlsx"  # Input file path (must contain a PaperId column)
OUTPUT_FILE = "snowball_output.xlsx"  # Output file path
# =============================================================================

sch = SemanticScholar()

# Limits and persistence settings
MAX_RESULTS_PER_DIRECTION = 2000  # Cap per direction per paper; adjust as needed
METADATA_BATCH_SIZE = 200
SAVE_EVERY = 200  # save checkpoint + append rows every N processed papers
STATE_PATH = "snowball_checkpoint.pkl"
CSV_TEMP_PATH = "snowball_temp.csv"  # Temporary CSV file


def _safe_collect_reference_ids(items):
    """Extract paperIds from Reference/Citation objects safely, capped per paper."""
    ids = []
    # items can be PaginatedResults (iterable) or list
    for item in itertools.islice(items or [], MAX_RESULTS_PER_DIRECTION):
        paper = getattr(item, "paper", None)
        pid = getattr(paper, "paperId", None)
        if pid:
            ids.append(str(pid))
    return ids


def _fallback_collect_from_paper(pid, have_backward, have_forward):
    """Fallback to the generic get_paper endpoint when the paginated ones fail."""
    backward = []
    forward = []
    try:
        paper = sch.get_paper(
            pid,
            fields=[
                "references.paperId",
                "citations.paperId",
                "referenceCount",
                "citationCount",
            ],
        )
        ref_count = getattr(paper, "referenceCount", None)
        cit_count = getattr(paper, "citationCount", None)

        if not have_backward and getattr(paper, "references", None):
            backward = [
                str(ref.paperId)
                for ref in paper.references
                if getattr(ref, "paperId", None)
            ]
            if ref_count and not backward:
                print(
                    f"    referenceCount={ref_count} but no reference ids returned for {pid}"
                )

        if not have_forward and getattr(paper, "citations", None):
            forward = [
                str(cit.paperId)
                for cit in paper.citations
                if getattr(cit, "paperId", None)
            ]
            if cit_count and not forward:
                print(
                    f"    citationCount={cit_count} but no citation ids returned for {pid}"
                )
    except Exception as e:
        print(f"    Fallback get_paper failed for {pid}: {e}")

    return backward, forward


def get_neighbors(pid):
    """Return backward + forward paperId lists with retry + fallback."""
    backward = []
    forward = []
    errors = []

    try:
        refs = sch.get_paper_references(pid, fields=["paperId"], limit=1000)
        backward = _safe_collect_reference_ids(refs)
    except Exception as e:
        errors.append(f"references endpoint: {e}")

    try:
        cits = sch.get_paper_citations(pid, fields=["paperId"], limit=1000)
        forward = _safe_collect_reference_ids(cits)
    except Exception as e:
        errors.append(f"citations endpoint: {e}")

    # If endpoints failed or returned empty, fall back to the simpler paper lookup.
    if (not backward or not forward) and errors:
        fb_backward, fb_forward = _fallback_collect_from_paper(
            pid, have_backward=bool(backward), have_forward=bool(forward)
        )
        if not backward:
            backward = fb_backward
        if not forward:
            forward = fb_forward

    if errors and not backward and not forward:
        print(f"    Warnings for {pid}: {', '.join(errors)}")

    return backward, forward


def fetch_metadata(paper_ids):
    """Fetch title and DOI in batches."""
    meta = {}
    ids = list(paper_ids)
    for start in range(0, len(ids), METADATA_BATCH_SIZE):
        batch = ids[start : start + METADATA_BATCH_SIZE]
        try:
            papers = sch.get_papers(
                batch,
                fields=["paperId", "title", "externalIds"],
                return_not_found=True,
            )
        except Exception as e:
            print(f"    Metadata batch failed ({start}-{start+len(batch)}): {e}")
            continue

        if isinstance(papers, tuple):
            papers, _missing = papers

        for p in papers:
            pid = str(getattr(p, "paperId", None) or "")
            if not pid:
                continue
            ext = getattr(p, "externalIds", {}) or {}
            doi = ext.get("DOI") or getattr(p, "doi", None)
            title = getattr(p, "title", None)
            meta[pid] = {
                "Title": title or "",
                "DOI": doi or "",
            }
    return meta


def save_state(state):
    with open(STATE_PATH, "wb") as f:
        pickle.dump(state, f)


def load_state():
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Failed to load checkpoint {STATE_PATH}: {e}")
    return None


def append_records(record_ids, paper_sources, all_backward, all_forward):
    """Append records for given ids to the temp CSV."""
    if not record_ids:
        return

    meta = fetch_metadata(record_ids)

    records = []
    for pid in record_ids:
        sources = paper_sources.get(pid, [])
        is_backward = 1 if pid in all_backward else 0
        is_forward = 1 if pid in all_forward else 0

        source_papers = list(set([s[0] for s in sources]))[:5]
        source_types = []
        if is_backward:
            source_types.append("Backward")
        if is_forward:
            source_types.append("Forward")

        rec_meta = meta.get(pid, {})
        records.append(
            {
                "PaperId": pid,
                "Title": rec_meta.get("Title", ""),
                "DOI": rec_meta.get("DOI", ""),
                "Direction": " + ".join(source_types),
                "IsBackward": is_backward,
                "IsForward": is_forward,
                "SourceCount": len(sources),
                "SourcePapers": "; ".join(source_papers),
            }
        )

    out_df = pd.DataFrame(records)
    header = not os.path.exists(CSV_TEMP_PATH)
    out_df.to_csv(CSV_TEMP_PATH, mode="a", index=False, header=header)


def run_snowballing(paper_ids, processed_ids, resume_state=None):
    """
    paper_ids: ids to snowball
    processed_ids: ids already processed (to exclude)
    resume_state: checkpoint dict if resuming
    """
    if resume_state:
        pending_ids = resume_state["pending_ids"]
        total_papers = resume_state["total_papers"]
        all_backward = resume_state["all_backward"]
        all_forward = resume_state["all_forward"]
        round_new_ids = resume_state["round_new_ids"]
        paper_sources = resume_state["paper_sources"]
        processed_in_round = resume_state["processed_in_round"]
        buffer_new_ids = resume_state["buffer_new_ids"]
    else:
        pending_ids = list(paper_ids)[::-1]  # stack
        total_papers = len(pending_ids)
        all_backward = set()
        all_forward = set()
        round_new_ids = set()
        paper_sources = {}
        processed_in_round = 0
        buffer_new_ids = []

    print(f"  Processing {total_papers} papers...")
    print(f"  Already processed papers (to exclude): {len(processed_ids)}")

    while pending_ids:
        pid = pending_ids.pop()
        processed_in_round += 1
        print(f"  [{processed_in_round}/{total_papers}] Fetching: {pid}")
        backward, forward = get_neighbors(pid)

        # Dedup + exclude already processed right away
        for b_pid in backward:
            if b_pid in processed_ids or b_pid in round_new_ids:
                continue
            paper_sources.setdefault(b_pid, []).append((pid, "backward"))
            round_new_ids.add(b_pid)
            all_backward.add(b_pid)
            buffer_new_ids.append(b_pid)

        for f_pid in forward:
            if f_pid in processed_ids or f_pid in round_new_ids:
                continue
            paper_sources.setdefault(f_pid, []).append((pid, "forward"))
            round_new_ids.add(f_pid)
            all_forward.add(f_pid)
            buffer_new_ids.append(f_pid)

        print(
            f"    -> Backward: {len(backward)}, Forward: {len(forward)}, new_total: {len(round_new_ids)}"
        )
        time.sleep(1)

        # Flush every SAVE_EVERY or when finished
        if processed_in_round % SAVE_EVERY == 0 or not pending_ids:
            append_records(
                buffer_new_ids, paper_sources, all_backward, all_forward
            )
            buffer_new_ids = []
            save_state(
                {
                    "pending_ids": pending_ids,
                    "total_papers": total_papers,
                    "all_backward": all_backward,
                    "all_forward": all_forward,
                    "round_new_ids": round_new_ids,
                    "paper_sources": paper_sources,
                    "processed_in_round": processed_in_round,
                    "buffer_new_ids": buffer_new_ids,
                    "processed_ids": processed_ids,
                }
            )

    combined = list(round_new_ids)

    # Ensure any remaining buffer was written (should be empty)
    if buffer_new_ids:
        append_records(buffer_new_ids, paper_sources, all_backward, all_forward)

    # Finalize CSV -> Excel
    if os.path.exists(CSV_TEMP_PATH):
        pd.read_csv(CSV_TEMP_PATH).to_excel(OUTPUT_FILE, index=False)
        os.remove(CSV_TEMP_PATH)
        print(f"  [Saved] {OUTPUT_FILE}")
    else:
        pd.DataFrame(
            columns=[
                "PaperId",
                "Title",
                "DOI",
                "Direction",
                "IsBackward",
                "IsForward",
                "SourceCount",
                "SourcePapers",
            ]
        ).to_excel(OUTPUT_FILE, index=False)
        print(f"  [Saved empty] {OUTPUT_FILE}")

    # Clear state checkpoint
    if os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)

    return combined, len(all_backward), len(all_forward)


def main():
    # Load seed paper ids and drop empties (including empty strings / 'nan')
    print(f"Loading input file: {INPUT_FILE}")
    df = pd.read_excel(INPUT_FILE)
    seed_ids = (
        df["PaperId"]
        .dropna()
        .astype(str)
        .str.strip()
    )
    seed_ids = [pid for pid in seed_ids if pid and pid.lower() != "nan"]
    seed_ids = list(dict.fromkeys(seed_ids))  # keep order while dedup
    
    state = load_state()

    # Check if output already exists
    if os.path.exists(OUTPUT_FILE) and not state:
        print(f"Output file {OUTPUT_FILE} already exists. Delete it to re-run.")
        return

    # Determine starting point
    if state:
        all_processed = set(state.get("processed_ids", seed_ids))
        print(f"Resuming from checkpoint: pending {len(state['pending_ids'])} papers")
    else:
        all_processed = set(seed_ids)

    print("\n" + "=" * 60)
    print("Snowballing (1 round)...")
    print(f"Seed papers: {len(seed_ids)}")
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 60)

    new_ids, b_count, f_count = run_snowballing(
        seed_ids, all_processed, state
    )
    all_processed.update(new_ids)

    # Write stats
    stats_file = OUTPUT_FILE.replace(".xlsx", "_stats.txt")
    with open(stats_file, "w", encoding="utf-8") as f:
        f.write(f"Initial seed papers: {len(seed_ids)}\n")
        f.write(f"Backward papers found: {b_count}\n")
        f.write(f"Forward papers found: {f_count}\n")
        f.write(f"Total new papers: {len(new_ids)}\n")
        f.write(f"Total unique papers (including seeds): {len(all_processed)}\n")

    print("\n" + "=" * 60)
    print("Snowballing complete!")
    print("=" * 60)
    print(f"Initial seed papers: {len(seed_ids)}")
    print(f"Backward papers found: {b_count}")
    print(f"Forward papers found: {f_count}")
    print(f"Total new papers: {len(new_ids)}")
    print(f"Total unique papers (including seeds): {len(all_processed)}")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(f"Stats saved to: {stats_file}")
    print("=" * 60)

    if os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)


if __name__ == "__main__":
    main()
