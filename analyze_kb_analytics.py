import json
import os
import glob
from collections import Counter
from typing import List, Dict, Any

def analyze_kb_analytics(log_dir: str):
    """Parses NDJSON logs and generates key insights."""
    log_files = glob.glob(os.path.join(log_dir, "*.ndjson"))
    entries = []
    
    for log_file in log_files:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    if not entries:
        return "No analytics data found."
    
    total = len(entries)
    found = [e for e in entries if e.get("answer_found") is True]
    not_found = [e for e in entries if e.get("answer_found") is False]
    
    # Insights
    top_docs = Counter()
    for e in entries:
        for cit in e.get("citations", []):
            top_docs[cit] += 1
            
    languages = Counter([e.get("detected_language") for e in entries])
    
    # Group by topic for missing content (simple keyword extraction)
    missing_topics = Counter([e.get("query").lower().split()[0] for e in not_found if e.get("query")])
    
    report = {
        "summary": {
            "total_queries": total,
            "fulfillment_rate": f"{(len(found)/total)*100:.2f}%",
            "gap_rate": f"{(len(not_found)/total)*100:.2f}%"
        },
        "top_cited_modules": top_docs.most_common(5),
        "language_distribution": languages.most_common(),
        "potential_knowledge_gaps": missing_topics.most_common(5),
        "last_10_unanswered": [e.get("query") for e in not_found[-10:]]
    }
    
    return json.dumps(report, indent=2)

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    analytics_dir = os.path.join(base_dir, "kb", "analytics")
    print(analyze_kb_analytics(analytics_dir))
