import os, json, math, re
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(__file__)
KB_DIR = os.path.join(BASE_DIR, "kb")
CHUNKS_PATH = os.path.join(KB_DIR, "kb_chunks.jsonl")
INDEX_PATH = os.path.join(KB_DIR, "kb_index.json")

WORD_RE = re.compile(r"[A-Za-z0-9_]+(?:'[A-Za-z0-9_]+)?")

class KBSearcher:
    def __init__(self, chunks_path=CHUNKS_PATH, index_path=INDEX_PATH):
        self.chunks_path = chunks_path
        self.index_path = index_path
        self._chunks = None
        self._vocab = None
        self._idf = None
        self._vectors = None
        self._inverted_index = None
        self._initialized = False

    def _initialize(self):
        if self._initialized:
            return True
        
        if not os.path.exists(self.chunks_path) or not os.path.exists(self.index_path):
            return False

        # Load chunks
        self._chunks = []
        with open(self.chunks_path, "r", encoding="utf-8") as r:
            for line in r:
                self._chunks.append(json.loads(line))

        # Load index
        with open(self.index_path, "r", encoding="utf-8") as r:
            index = json.load(r)
            self._vocab = index["vocab"]
            self._idf = index["idf"]
            self._vectors = index["vectors"]

        # Build inverted index and pre-normalize vectors for faster dot product (cosine equivalent)
        self._inverted_index = defaultdict(list)
        for i, dv in enumerate(self._vectors):
            # Pre-calculate norm to normalize on the fly if ingest didn't
            # This makes cosine similarity a simple dot product
            norm = math.sqrt(sum(v*v for v in dv.values())) or 1.0
            for k, v in dv.items():
                val_norm = v / norm
                dv[k] = val_norm
                self._inverted_index[int(k)].append((i, val_norm))
        
        self._initialized = True
        return True

    def _tokenize(self, text: str):
        return [w.lower() for w in WORD_RE.findall(text)]

    def _vec_from_query(self, query: str):
        tf = Counter(self._tokenize(query))
        vec = {}
        for t, cnt in tf.items():
            if t in self._vocab:
                # Store as integer key for faster lookup in inverted index
                i = int(self._vocab[t])
                vec[i] = cnt * self._idf[i]
        
        # Normalize query vector
        norm = math.sqrt(sum(v*v for v in vec.values())) or 1.0
        for k in list(vec.keys()):
            vec[k] /= norm
        return vec

    def search(self, query: str, top_k: int = 5):
        if not self._initialize():
            return {"ok": False, "error": "Index not built. Run kb_ingest first."}

        qv = self._vec_from_query(query)
        if not qv:
            return {"ok": True, "query": query, "top_k": top_k, "results": []}

        # Use inverted index to find candidate docs
        scores = defaultdict(float)
        for term_id, q_val in qv.items():
            if term_id in self._inverted_index:
                for doc_id, d_val in self._inverted_index[term_id]:
                    scores[doc_id] += q_val * d_val

        # Sort and return top_k
        scored = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max(1, top_k)]

        results = []
        for doc_id, score in scored:
            c = self._chunks[doc_id]
            results.append({
                "score": round(score, 6),
                "file": c["file"],
                "heading_path": c.get("heading_path", ""),
                "chunk_id": c.get("chunk_id", f"#{doc_id}"),
                "preview": (c["text"][:280] + "…") if len(c["text"]) > 280 else c["text"]
            })

        return {"ok": True, "query": query, "top_k": top_k, "results": results}

# Singleton instance for easy reuse
_searcher = KBSearcher()

def kb_search(query: str, top_k: int = 5):
    return _searcher.search(query, top_k)
