from app.store import add_document, get_collection, search


def test_search_finds_the_relevant_chunk(tmp_path):
    collection = get_collection(str(tmp_path / "db"))
    chunks = [
        {"page": 1, "chunk_index": 0, "text": "The capital of France is Paris."},
        {"page": 2, "chunk_index": 0, "text": "Photosynthesis lets plants turn sunlight into energy."},
    ]
    assert add_document(collection, "doc1", "facts.pdf", chunks) == 2

    hits = search(collection, "Which city is the French capital?", k=1)

    assert hits[0]["page"] == 1
    assert hits[0]["source"] == "facts.pdf"