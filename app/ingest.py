import io

import pdfplumber


def extract_pages(content: bytes) -> list[tuple[int, str]]:
    """Return (page_number, text) for every page that has text."""
    pages = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append((number, text))
    return pages


def chunk_text(text: str, size: int = 800, overlap: int = 150) -> list[str]:
    """Split text into chunks of about `size` characters that overlap."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def chunk_pages(pages: list[tuple[int, str]], size: int = 800, overlap: int = 150) -> list[dict]:
    """Chunk every page and keep the page number with each chunk."""
    result = []
    for page_number, text in pages:
        for index, chunk in enumerate(chunk_text(text, size, overlap)):
            result.append({"page": page_number, "chunk_index": index, "text": chunk})
    return result