from bs4 import BeautifulSoup
from pathlib import Path
import re

base_path = Path("./data/raw/sec-edgar-filings")
files = base_path.glob("*/10-K/**/*.txt")

output_path = Path("./data/processed")
output_path.mkdir(parents=True, exist_ok=True)

start_pattern = r"\bITEM\s+1A\s*[.\-–:]?\s*RISK\s+FACTORS\b"
end_pattern = r"\bITEM\s+1B\s*[.\-–:]?\s*UNRESOLVED\s+STAFF\s+COMMENTS\b"

for path in files: 
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    # clean = BeautifulSoup(raw, "html.parser").get_text(" ", strip=True)
    soup = BeautifulSoup(raw, "html.parser")

    for br in soup.find_all("br"):
        br.replace_with("\n")

    for tag in soup.find_all(["p", "div", "tr"]):
        tag.append("\n")

    clean = soup.get_text(separator="")

    clean = re.sub(r"[ \t]+", " ", clean)
    clean = re.sub(r" *\n *", "\n", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean)


    # first = raw.find("Item 1A")
    # second = raw.find("Item 1A", first + 1)
    # end = raw.find("Item 1B", second)

    # risk_factors = raw[second : end]

    #Find the beginning and end of A1 section
    starts = list(re.finditer(start_pattern, clean, re.IGNORECASE))
    ends = list(re.finditer(end_pattern, clean, re.IGNORECASE))

    if not starts:
        raise ValueError("Item 1A not found")

    #Get first position relative to 1A
    start = starts[-1].start()

    # Get end postion relative to 1B
    end = None
    for m in ends:
        if m.start() > start:
            end = m.start()

    risk_factors  = clean[start : end] if end else clean[start:]

    ticker = path.relative_to(base_path).parts[0]
    filing_id = path.parent.name

    save_path = output_path / f"{ticker}_{filing_id}_1A.txt"
    save_path.write_text(risk_factors, encoding="utf-8")