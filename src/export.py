import pandas as pd
from bm25 import get_results

themes = {
    "supply_chain": ["supply chain disruption", "supplier shortages", "component shortages"],
    "cybersecurity": ["cybersecurity breach", "data breach", "cyber attack"],
    "interest_rates": ["interest rate risk", "rising interest rates"],
}

rows = []
for theme, queries in themes.items():
    for q in queries:
        for rank, (doc, score) in enumerate(get_results(q, 200), start=1):
            rows.append({
                "theme": theme,
                "query": q,
                "rank": rank,
                "score": score,
                "company": doc.get("company"),
                "year": doc.get("year"),
                "text": doc["text"],
            })

pd.DataFrame(rows).to_csv("data/search_results.csv", index=False)