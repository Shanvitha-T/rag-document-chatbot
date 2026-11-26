import chromadb

COLLECTION = "documents"


def get_collection(path: str = "chroma_db"):
    client = chromadb.PersistentClient(path=path)
    return client.get_or_create_collection(COLLECTION)


def add_document(collection, doc_id: str, filename: str, chunks: list[dict]) -> int:
    """Store chunks for one document. Re-uploading the same doc_id replaces it."""
    if not chunks:
        return 0
    collection.upsert(
        ids=[f"{doc_id}-{c['page']}-{c['chunk_index']}" for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {"doc_id": doc_id, "source": filename, "page": c["page"]} for c in chunks
        ],
    )
    return len(chunks)


def search(collection, question: str, k: int = 4) -> list[dict]:
    """Return the k chunks closest in meaning to the question."""
    if collection.count() == 0:
        return []
    result = collection.query(query_texts=[question], n_results=min(k, collection.count()))
    hits = []
    for text, meta, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append(
            {
                "text": text,
                "source": meta["source"],
                "page": meta["page"],
                "distance": distance,
            }
        )
    return hits