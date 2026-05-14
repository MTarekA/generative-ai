from evaluate import normalize_text


def test_normalize_text() -> None:
    """
    Test text normalization used in evaluation.
    """
    text = "  Retrieval-Augmented Generation  "

    normalized = normalize_text(text)

    assert normalized == "retrieval-augmented generation"