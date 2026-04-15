"""
update_hma.py
Fetches the latest HMA (Harga Mineral Acuan) values from minerba.esdm.go.id
and updates the hma object in index.html.
Runs as part of the GitHub Actions workflow.
"""

import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta


URL = "https://www.minerba.esdm.go.id/harga_acuan"

# Commodity names as they appear in the page
COMMODITIES = {
    "Nikel": "nikel",
    "Bijih Besi Laterit/Hematit/Magnetit": "bijih_besi",
    "Kobalt": "kobalt",
    "Bijih Krom": "bijih_krom",
}

MONTH_ORDER = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]


def fetch_page():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_hma(html):
    """
    The page embeds HMA data as plain text numbers in the HTML.
    We find all period headers and all commodity rows, then pick the latest period column.
    """

    # Strip HTML tags helper
    def strip_tags(s):
        return re.sub(r"<[^>]+>", "", s).strip()

    # Find the main data table
    table_match = re.search(r"Tabel Harga Mineral dan Batubara Acuan.*?(<table.*?</table>)", html, re.DOTALL)
    if not table_match:
        raise ValueError("Could not find HMA table in page")

    table_html = table_match.group(1)

    # Extract all rows
    rows = re.findall(r"<tr.*?>(.*?)</tr>", table_html, re.DOTALL)
    if not rows:
        raise ValueError("No rows found in table")

    # First row = header with period labels
    header_cells = re.findall(r"<t[hd].*?>(.*?)</t[hd]>", rows[0], re.DOTALL)
    period_labels = [strip_tags(c) for c in header_cells]

    # Find the latest period index (last non-empty column header)
    latest_idx = None
    latest_label = None
    for i, label in enumerate(period_labels):
        if re.search(r"(Pertama|Kedua)", label):
            latest_idx = i
            latest_label = label

    if latest_idx is None:
        raise ValueError(f"Could not find period columns. Headers: {period_labels}")

    print(f"Found {len(period_labels)} columns. Latest: {latest_label} (index {latest_idx})")

    # Parse commodity rows
    hma_values = {}
    found = set()

    for row in rows[1:]:
        cells = re.findall(r"<t[hd].*?>(.*?)</t[hd]>", row, re.DOTALL)
        if not cells:
            continue
        row_label = strip_tags(cells[0])

        for commodity, key in COMMODITIES.items():
            if commodity in row_label and key not in found:
                if latest_idx < len(cells):
                    val_str = strip_tags(cells[latest_idx]).replace(",", ".")
                    try:
                        hma_values[key] = float(val_str)
                        found.add(key)
                        print(f"  {commodity}: {hma_values[key]}")
                    except ValueError:
                        raise ValueError(f"Could not parse value '{val_str}' for {commodity}")
                else:
                    raise ValueError(f"Column index {latest_idx} out of range for {commodity}")

    missing = set(COMMODITIES.values()) - found
    if missing:
        raise ValueError(f"Could not find data for: {missing}")

    return hma_values, latest_label


def update_index_html(hma_values, period_label):
    """Replace hma object and period label in index.html."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Update last-updated timestamp (WIB = UTC+7)
    wib = timezone(timedelta(hours=7))
    now_wib = datetime.now(wib).strftime("%Y-%m-%d %H:%M WIB")
    content = re.sub(
        r'const hmaUpdated = "[^"]*";',
        f'const hmaUpdated = "{now_wib}";',
        content
    )

    # Update hmaPeriod label
    short = period_label.replace("Periode Pertama", "P1").replace("Periode Kedua", "P2")
    short = short.replace("(", "").replace(")", "").strip()
    parts = short.split()
    period_short = f"{parts[0]} {parts[1]} ({parts[2]})"
    content = re.sub(
        r'const hmaPeriod = "[^"]*";',
        f'const hmaPeriod = "{period_short}";',
        content
    )

    # Update hma values
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

    # Determine short label e.g. "April 2026 (Periode Kedua)" -> "April 2026 (P2)"
    short = period_label.replace("Periode Pertama", "P1").replace("Periode Kedua", "P2")
    short = short.replace("(", "").replace(")", "").strip()
    parts = short.split()  # ['April', '2026', 'P2']

    card_title = f"HMA \u2014 {parts[0]} {parts[1]} ({parts[2]})"
    content = re.sub(
        r"HMA\s*\u2014\s*\w+\s+\d{4}\s+\(P[12]\)",
        card_title,
        content
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nindex.html updated:")
    print(f"  Period : {card_title}")
    print(f"  Values : {hma_values}")


if __name__ == "__main__":
    try:
        html = fetch_page()
        hma_values, period_label = parse_hma(html)
        update_index_html(hma_values, period_label)
        print("\nDone.")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
