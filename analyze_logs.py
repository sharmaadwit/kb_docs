import json
import os
import glob
from collections import Counter

def analyze_logs(log_dir):
    log_files = glob.glob(os.path.join(log_dir, "*.ndjson"))
    all_entries = []
    
    for log_file in log_files:
        with open(log_file, "r") as f:
            for line in f:
                if line.strip():
                    all_entries.append(json.loads(line))
    
    total_queries = len(all_entries)
    if total_queries == 0:
        return "No log entries found."
        
    unanswered = [e for e in all_entries if e.get("unanswered") is True]
    latencies = [e.get("latency_ms", 0) for e in all_entries]
    scores = [e.get("top_score", 0) for e in all_entries]
    
    users = [e.get("user_email") for e in all_entries]
    user_counts = Counter(users)
    
    citations = []
    for e in all_entries:
        for cit in e.get("citations", []):
            citations.append(cit.get("path"))
    citation_counts = Counter(citations)
    
    report = {
        "summary": {
            "total_queries": total_queries,
            "unanswered_count": len(unanswered),
            "unanswered_rate": f"{(len(unanswered)/total_queries)*100:.2f}%",
            "avg_latency_ms": sum(latencies)/total_queries,
            "avg_confidence_score": sum(scores)/total_queries
        },
        "top_users": user_counts.most_common(5),
        "top_cited_docs": citation_counts.most_common(5),
        "unanswered_details": [e.get("query") for e in unanswered]
    }
    
    return json.dumps(report, indent=2)

if __name__ == "__main__":
    log_directory = "/Users/md files/drive-download-20260219T070629Z-3-001/kb/analytics"
    print(analyze_logs(log_directory))
