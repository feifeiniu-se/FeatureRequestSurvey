"""
Script 1: Automatically obtain DOI and Semantic Scholar PaperId
based on Title + Year.

Input:  ForSnowballing.xlsx (must contain at least "Title" and
    "Publication Year" columns)
Output: papers_with_ids.xlsx
"""

from semanticscholar import SemanticScholar
import pandas as pd
import time

sch = SemanticScholar()

# Manual override table to avoid matching incorrect papers
MANUAL_OVERRIDES = {
    "assigning change requests to software developers": {
        "DOI": "10.1002/smr.530",
        "PaperId": "7f9082e47fbb0829426b4c91c7bcc9f0c09718b8",
    }
}


def normalize_title(value: str) -> str:
    return (value or "").strip().lower()


# 1. Read the source Excel file
df = pd.read_excel("ForSnowballing.xlsx")  # Make sure this file is in the current directory

results = []

for idx, row in df.iterrows():
    title = str(row["Title"]).strip()
    year_raw = row.get("Publication Year", "")
    year = int(year_raw) if pd.notna(year_raw) else None
    key = normalize_title(title)

    # Apply manual override first if available
    if key in MANUAL_OVERRIDES:
        override = MANUAL_OVERRIDES[key]
        results.append(
            {
                "Title": title,
                "Year": year,
                "DOI": override["DOI"],
                "PaperId": override["PaperId"],
                "LookupStatus": "manual-fixed",
            }
        )
        print(f"[MANUAL] {title} -> DOI: {override['DOI']}")
        continue

    print("Searching:", title, "(", year if year is not None else "N/A", ")")

    try:
        # Search papers on Semantic Scholar
        kwargs = {"title": title}
        if year is not None:
            kwargs["year"] = year
        papers = sch.search_paper(title, year=year) if year is not None else sch.search_paper(title)
        if papers:
            p = papers[0]  # Take the most relevant result

            # Safely obtain DOI and PaperId
            doi = ""
            ext_ids = getattr(p, "externalIds", {}) or {}
            doi = ext_ids.get("DOI") or getattr(p, "doi", "") or ""
            paper_id = getattr(p, "paperId", "") or ""

            results.append(
                {
                    "Title": title,
                    "Year": year,
                    "DOI": doi,
                    "PaperId": paper_id,
                    "LookupStatus": "ok",
                }
            )
            print(f"[OK] {title} -> DOI: {doi or 'N/A'}")
        else:
            results.append(
                {
                    "Title": title,
                    "Year": year,
                    "DOI": "",
                    "PaperId": "",
                    "LookupStatus": "not-found",
                }
            )
            print(f"[NOT FOUND] {title}")

    except Exception as e:
        print("Error:", e)
        results.append(
            {
                "Title": title,
                "Year": year,
                "DOI": "",
                "PaperId": "",
                "LookupStatus": f"error:{e}",
            }
        )

    time.sleep(1)  # Avoid hitting API rate limits

# Save results to Excel
out_df = pd.DataFrame(results)
out_df.to_excel("papers_with_ids.xlsx", index=False)

print("\nSaved: papers_with_ids.xlsx")
