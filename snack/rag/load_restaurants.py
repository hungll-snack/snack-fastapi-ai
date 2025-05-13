# rag/load_restaurants.py

import os
import requests
from rag.embedder import get_embedding
from rag.faiss_index import save_faiss_index

DJANGO_URL = os.getenv("DJANGO_BASE_URL", "http://localhost:8000")

def fetch_restaurants():
    res = requests.get(f"{DJANGO_URL}/restaurant/all")
    return res.json()

def build_and_save_faiss():
    data = fetch_restaurants()

    texts = []
    metadata = []

    for r in data:
        keyword = r.get("keyword", "")
        if not keyword:
            continue
        texts.append(keyword)
        metadata.append({
            "name": r["name"],
            "address": r["address"],
            "rating": r.get("rating", None)
        })

    embeddings = [get_embedding(text) for text in texts]
    save_faiss_index(embeddings, metadata)

if __name__ == "__main__":
    build_and_save_faiss()
