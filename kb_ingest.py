import os, json, math, re
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(__file__)
KB_DIR = os.path.join(BASE_DIR, "kb")
CHUNKS_PATH = os.path.join(KB_DIR, "kb_chunks.jsonl")
INDEX_PATH = os.path.join(KB_DIR, "kb_index.json")

WORD_RE = re.compile(r"[A-Za-z0-9_]+(?:'[A-Za-z0-9_]+)?")

def _tokenize(text):
    return [w.lower() for w in WORD_RE.findall(text)]

def _get_heading_path(line, current_path):
    match = re.match(r"^(#+)\s+(.+)$", line)
    if not match:
        return current_path
    
    level = len(match.group(1))
    title = match.group(2).strip()
    
    new_path = current_path[:level-1]
    new_path.append(title)
    return new_path

def kb_ingest(force_rebuild=False, chunk_chars=2800, overlap_chars=450):
    if not force_rebuild and os.path.exists(CHUNKS_PATH) and os.path.exists(INDEX_PATH):
        return {"ok": True, "message": "Index already exists. Use force_rebuild=True to overwrite."}

    if not os.path.exists(KB_DIR):
        os.makedirs(KB_DIR)

    chunks = []
    file_count = 0
    
    for filename in os.listdir(KB_DIR):
        if not filename.endswith(".md"):
            continue
        
        file_count += 1
        filepath = os.path.join(KB_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Simple chunking by headings and character limit
            lines = content.splitlines()
            current_path = []
            current_chunk_text = []
            current_chunk_size = 0
            
            for line in lines:
                current_path = _get_heading_path(line, current_path)
                line_size = len(line) + 1
                
                if current_chunk_size + line_size > chunk_chars and current_chunk_text:
                    # Save chunk
                    chunks.append({
                        "file": filename,
                        "heading_path": " > ".join(current_path),
                        "text": "\n".join(current_chunk_text),
                        "chunk_id": f"{filename}#L{len(chunks)}"
                    })
                    # Keep some overlap
                    overlap_lines = current_chunk_text[-5:] if len(current_chunk_text) > 5 else []
                    current_chunk_text = overlap_lines + [line]
                    current_chunk_size = sum(len(l)+1 for l in current_chunk_text)
                else:
                    current_chunk_text.append(line)
                    current_chunk_size += line_size
            
            if current_chunk_text:
                chunks.append({
                    "file": filename,
                    "heading_path": " > ".join(current_path),
                    "text": "\n".join(current_chunk_text),
                    "chunk_id": f"{filename}#L{len(chunks)}"
                })

    # Save chunks
    with open(CHUNKS_PATH, "w", encoding="utf-8") as w:
        for c in chunks:
            w.write(json.dumps(c) + "\n")

    # TF-IDF Calculation
    vocab = {}
    df = Counter()
    doc_tfs = []
    
    for c in chunks:
        tokens = _tokenize(c["text"])
        tf = Counter(tokens)
        doc_tfs.append(tf)
        for t in tf:
            df[t] += 1
            if t not in vocab:
                vocab[t] = len(vocab)

    n_docs = len(chunks)
    idf = [0.0] * len(vocab)
    for t, idx in vocab.items():
        idf[idx] = math.log10(n_docs / (df[t] or 1))

    vectors = []
    for tf in doc_tfs:
        vec = {}
        for t, count in tf.items():
            idx = vocab[t]
            vec[idx] = count * idf[idx]
        vectors.append(vec)

    index = {
        "vocab": vocab,
        "idf": idf,
        "vectors": vectors,
        "metadata": {
            "file_count": file_count,
            "chunk_count": len(chunks),
            "vocab_size": len(vocab)
        }
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as w:
        json.dump(index, w)

    return {
        "ok": True, 
        "file_count": file_count, 
        "chunk_count": len(chunks), 
        "vocab_size": len(vocab)
    }

if __name__ == "__main__":
    print(kb_ingest(force_rebuild=True))
