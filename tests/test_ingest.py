from app.ingest import chunk_pages, chunk_text


def test_short_text_is_one_chunk():
    assert chunk_text("hello world", size=800, overlap=150) == ["hello world"]


def test_long_text_is_split_with_overlap():
    text = "a" * 2000
    chunks = chunk_text(text, size=800, overlap=150)
    assert len(chunks) == 3
    assert all(len(c) <= 800 for c in chunks)


def test_page_numbers_are_kept():
    result = chunk_pages([(1, "first page"), (2, "second page")])
    assert [r["page"] for r in result] == [1, 2]