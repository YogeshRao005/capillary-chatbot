# rebuild_index.py
# Build FAISS index from data/docs.jsonl using sentence-transformers
import os, json, sys
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

DOCS_FILE = "data/docs.jsonl"
INDEX_DIR = "data/faiss_index"
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "metadata.json")

os.makedirs(INDEX_DIR, exist_ok=True)

if not os.path.exists(DOCS_FILE):
    print(f"ERROR: {DOCS_FILE} not found. Run scraper.py first.")
    sys.exit(1)

texts, urls, titles = [], [], []
with open(DOCS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        txt = (obj.get("text") or "").strip()
        if len(txt) < 30:
            continue
        texts.append(txt)
        urls.append(obj.get("url",""))
        titles.append(obj.get("title",""))

print("Loaded", len(texts), "documents.")

if len(texts) == 0:
    print("No documents to index. Exiting.")
    sys.exit(1)

print("Loading embedding model (all-MiniLM-L6-v2, CPU)...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

print("Creating embeddings (this may take a while)...")
emb = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
emb = np.array(emb, dtype=np.float32)
print("Embeddings shape:", emb.shape)

print("Building FAISS index (L2)...")
dim = emb.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(emb)
print("Index total vectors:", index.ntotal)

print("Saving index and metadata...")
faiss.write_index(index, INDEX_FILE)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump({"urls": urls, "titles": titles}, f, ensure_ascii=False, indent=2)

size_kb = os.path.getsize(INDEX_FILE) / 1024.0
print(f"✅ index saved: {INDEX_FILE} ({size_kb:.2f} KB)")
print(f"✅ metadata saved: {META_FILE}")
