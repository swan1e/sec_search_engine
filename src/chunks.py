from pathlib import Path
import json

base_path = Path("./data/processed")
files = sorted(base_path.glob("*.txt"))

all_chunks = []

for file in files:
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    lines = raw.split("\n")

    cleaned = []
    for line in lines:
        s = line.strip()
        if "Form 10-K" in s:
            continue
        if s == "Item 1A.":
            continue
        if s == "Risk Factors":
            continue
        if s:
            cleaned.append(s)

    parts = file.name.split("_")
    company = parts[0]
    year = int(parts[1].split("-")[1]) + 2000

    for i, text in enumerate(cleaned):
        all_chunks.append({
            "chunk_id": f"{company}_{year}_{i:03d}",
            "company": company,
            "year": year,
            "text": text,
        })

with open("./data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)