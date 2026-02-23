import os
import json
import glob
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from collections import Counter

app = FastAPI()

LOG_DIR = "kb/analytics"

def get_aggregated_stats():
    log_files = glob.glob(os.path.join(LOG_DIR, "*.ndjson"))
    entries = []
    for f_path in log_files:
        with open(f_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    if not entries:
        return None
        
    total = len(entries)
    unanswered = [e for e in entries if e.get("unanswered") is True]
    latencies = [e.get("latency_ms", 0) for e in entries]
    scores = [e.get("top_score", 0) for e in entries]
    
    user_counts = Counter([e.get("user_email") for e in entries])
    
    citations = []
    for e in entries:
        for cit in e.get("citations", []):
            citations.append(cit.get("path"))
    doc_counts = Counter(citations)
    
    # Timeline data (simple aggregation by date)
    # In a real app we'd use the 'ts' field more precisely
    
    return {
        "summary": {
            "total_queries": total,
            "success_rate": f"{((total - len(unanswered))/total)*100:.1f}%",
            "avg_latency": f"{sum(latencies)/total:.0f}ms",
            "avg_score": f"{sum(scores)/total:.2f}"
        },
        "top_users": [{"email": u, "count": c} for u, c in user_counts.most_common(5)],
        "top_docs": [{"path": p, "count": c} for p, c in doc_counts.most_common(5)],
        "recent_queries": [{"query": e.get("query"), "user": e.get("user_email"), "ts": e.get("ts")} for e in entries[-10:]]
    }

@app.get("/api/stats")
async def stats():
    return get_aggregated_stats()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
