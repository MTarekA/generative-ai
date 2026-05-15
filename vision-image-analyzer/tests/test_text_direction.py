from streamlit_app import is_arabic_text


def test_is_arabic_text_detects_arabic() -> None:
    """
    Test Arabic text detection.
    """
    assert is_arabic_text("اشرحلي الصورة دي") is True


def test_is_arabic_text_detects_english() -> None:
    """
    Test non-Arabic text detection.
    """
    assert is_arabic_text("Analyze this image") is False