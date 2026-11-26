from types import SimpleNamespace

from app.qa import NOT_FOUND, answer_question, build_context


class FakeClient:
    def __init__(self, reply):
        self.messages = SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
            content=[SimpleNamespace(type="text", text=reply)]
        ))


HITS = [{"text": "Paris is the capital of France.", "source": "facts.pdf", "page": 3, "distance": 0.1}]


def test_no_hits_returns_not_found_without_calling_claude():
    assert answer_question("anything", [], client=None) == {"answer": NOT_FOUND, "sources": []}


def test_context_is_numbered_with_page():
    assert "[1] (facts.pdf, page 3)" in build_context(HITS)


def test_answer_and_sources_are_returned():
    result = answer_question("Capital of France?", HITS, client=FakeClient("Paris [1]"))
    assert result["answer"] == "Paris [1]"
    assert result["sources"][0]["page"] == 3
    