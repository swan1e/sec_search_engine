from bs4 import BeautifulSoup
import re

path = "./data/raw/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    raw = f.read()

clean = BeautifulSoup(raw, "html.parser").get_text(" ", strip=True)

# first = raw.find("Item 1A")
# second = raw.find("Item 1A", first + 1)
# end = raw.find("Item 1B", second)

# risk_factors = raw[second : end]

#Find the beginning and end of A1 section
start_pattern = r"\bITEM\s+1A\s*[.\-–:]?\s*RISK\s+FACTORS\b"
end_pattern = r"\bITEM\s+1B\s*[.\-–:]?\s*UNRESOLVED\s+STAFF\s+COMMENTS\b"

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
print(risk_factors[:500])


