from streamlit_app import is_arabic_text


def test_is_arabic_text_detects_arabic() -> None:
    """
    Test Arabic text detection.
    """
    assert is_arabic_text("ده نص عربي") is True


def test_is_arabic_text_detects_english() -> None:
    """
    Test non-Arabic text detection.
    """
    assert is_arabic_text("This is English text") is False