"""
update_hma.py
Fetches the latest HMA (Harga Mineral Acuan) values from minerba.esdm.go.id
and updates the hma object in index.html.
Runs as part of the GitHub Actions workflow.
"""

import re
import sys
import json
import urllib.request
from datetime import datetime

URL = "https://www.minerba.esdm.go.id/harga_acuan"

# Map from minerba commodity labels to our hma keys
COMMODITY_MAP = {
    "Nikel": "nikel",
    "Bijih Besi Laterit/Hematit/Magnetit": "bijih_besi",
    "Kobalt": "kobalt",
    "Bijih Krom": "bijih_krom",
}


def fetch_hma():
    """Scrape HMA table from minerba and return the latest periode values."""
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8")

    # The page renders data as JSON inside a <script> tag or as JS arrays.
    # The table columns correspond to periods in chronological order.
    # We find the JS data arrays for each commodity.

    # Pattern: find the harga_acuan data block - it's rendered as chart data
    # Each commodity row in the table is: name, then values per period
    # We parse the table by finding period headers and commodity rows.

    # Find all period labels (e.g. "April 2026 (Periode Kedua)")
    period_labels = re.findall(
        r'(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
        r'\s+\d{4}\s+\(Periode\s+(?:Pertama|Kedua)\)',
        html
    )

    if not period_labels:
        raise ValueError("Could not find period labels on page")

    # Remove duplicates while preserving order
    seen = set()
    unique_periods = []
    for p in period_labels:
        if p not in seen:
            seen.add(p)
            unique_periods.append(p)

    print(f"Found {len(unique_periods)} periods. Latest: {unique_periods[-1]}")
    latest_period = unique_periods[-1]
    latest_index = len(unique_periods) - 1  # 0-based index of latest period

    # Now find each commodity's data row
    # The table data is embedded as JSON for charts - find dataset arrays
    # Pattern: "label":"Nikel","data":[val1,val2,...,valN]
    hma_values = {}

    for label, key in COMMODITY_MAP.items():
        # Escape for regex
        escaped = re.escape(label)
        # Match the data array associated with this commodity in chart JSON
        pattern = rf'"label"\s*:\s*"{escaped}"[^}}]*?"data"\s*:\s*\[([^\]]+)\]'
        match = re.search(pattern, html)
        if match:
            values_str = match.group(1)
            values = [float(v.strip()) for v in values_str.split(",") if v.strip()]
            if latest_index < len(values):
                hma_values[key] = values[latest_index]
                print(f"  {label}: {values[latest_index]}")
            else:
                raise ValueError(f"Index {latest_index} out of range for {label} (has {len(values)} values)")
        else:
            raise ValueError(f"Could not find data for commodity: {label}")

    return hma_values, latest_period


def update_index_html(hma_values, period_label):
    """Replace hma object and period label in index.html."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Update hma object
    new_hma_line = (
        f"  nikel: {hma_values['nikel']}, "
        f"bijih_besi: {hma_values['bijih_besi']}, "
        f"kobalt: {hma_values['kobalt']}, "
        f"bijih_krom: {hma_values['bijih_krom']},"
    )
    content = re.sub(
        r"nikel:\s*[\d.]+,\s*bijih_besi:\s*[\d.]+,\s*kobalt:\s*[\d.]+,\s*bijih_krom:\s*[\d.]+,",
        new_hma_line,
        content
    )

    # Update HMA card title — determine short period label
    # e.g. "April 2026 (Periode Kedua)" -> "April 2026 (P2)"
    short_label = period_label.replace("Periode Pertama", "P1").replace("Periode Kedua", "P2")
    short_label = short_label.replace("(", "").replace(")", "").strip()
    parts = short_label.split()
    # parts: ['April', '2026', 'P2']
    card_title = f"HMA — {parts[0]} {parts[1]} ({parts[2]})"

    content = re.sub(
        r'HMA\s*—\s*\w+\s+\d{4}\s+\(P[12]\)',
        card_title,
        content
    )

    # Update header subtitle date
    # "Berlaku 16–30 April 2026" or "Berlaku 1–15 April 2026"
    month_year = f"{parts[0]} {parts[1]}"
    if "P1" in parts:
        berlaku = f"Berlaku 1–15 {month_year}"
    else:
        berlaku = f"Berlaku 16–30 {month_year}"

    content = re.sub(
        r'Berlaku[\s\d–-]+\w+\s+\d{4}',
        berlaku,
        content
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nindex.html updated:")
    print(f"  Period: {card_title}")
    print(f"  Header: {berlaku}")
    print(f"  HMA values: {hma_values}")


if __name__ == "__main__":
    try:
        hma_values, period_label = fetch_hma()
        update_index_html(hma_values, period_label)
        print("\nDone.")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
