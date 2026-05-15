import json
from pathlib import Path

import streamlit as st

from app.audio_loader import AudioLoader
from app.config import UPLOADED_AUDIO_DIR, ensure_directories
from app.result_manager import ResultManager
from app.summarization_pipeline import SummarizationPipeline
from app.transcription_pipeline import TranscriptionPipeline


st.set_page_config(
    page_title="AI Voice Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
)


def apply_custom_styles() -> None:
    """
    Apply custom CSS styles to improve UI and Arabic RTL rendering.
    """
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 3rem;
            padding-bottom: 6rem;
            max-width: 1200px;
        }

        [data-testid="stSidebar"] {
            background-color: #f7f9fc;
        }

        .rtl-text {
            direction: rtl;
            text-align: right;
            line-height: 1.9;
            font-size: 1rem;
            unicode-bidi: plaintext;
        }

        .ltr-text {
            direction: ltr;
            text-align: left;
            line-height: 1.7;
            font-size: 1rem;
            unicode-bidi: plaintext;
        }

        .metadata-box {
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_arabic_text(text: str) -> bool:
    """
    Detect whether the given text contains Arabic characters.
    """
    return any("\u0600" <= char <= "\u06FF" for char in text)


def render_text_with_direction(text: str) -> None:
    """
    Render text with RTL support for Arabic and LTR for other languages.
    """
    css_class = "rtl-text" if is_arabic_text(text) else "ltr-text"

    st.markdown(
        f'<div class="{css_class}">{text}</div>',
        unsafe_allow_html=True,
    )


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.
    """
    if "current_audio_path" not in st.session_state:
        st.session_state.current_audio_path = None

    if "current_audio_name" not in st.session_state:
        st.session_state.current_audio_name = None

    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None


def save_uploaded_audio(uploaded_file) -> Path:
    """
    Save uploaded audio file to the uploaded audio directory.
    """
    ensure_directories()

    file_path = UPLOADED_AUDIO_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def render_audio_metadata(metadata: dict) -> None:
    """
    Render audio metadata in a readable format.
    """
    st.markdown('<div class="metadata-box">', unsafe_allow_html=True)

    st.subheader("Audio Metadata")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("File Size MB", metadata.get("file_size_mb", "N/A"))

    with col2:
        st.metric("Extension", metadata.get("file_extension", "N/A"))

    st.write(f"File name: {metadata.get('file_name', 'unknown')}")
    st.write(f"File size bytes: {metadata.get('file_size_bytes', 'unknown')}")

    st.markdown("</div>", unsafe_allow_html=True)


def create_downloadable_result(result: dict) -> str:
    """
    Convert latest result to a JSON string for download.
    """
    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )


def analyze_audio(audio_path: Path) -> None:
    """
    Run transcription, summarization, and result saving.
    """
    try:
        with st.spinner("Transcribing audio..."):
            transcription_pipeline = TranscriptionPipeline()
            transcription_response = transcription_pipeline.transcribe_audio(
                audio_path
            )

        with st.spinner("Summarizing transcript..."):
            summarization_pipeline = SummarizationPipeline()
            summary_response = summarization_pipeline.summarize_transcript(
                transcription_response.transcript
            )

        result_manager = ResultManager()
        saved_result_path = result_manager.save_audio_analysis_result(
            audio_path=audio_path,
            transcript=transcription_response.transcript,
            summary=summary_response.summary,
            audio_metadata=transcription_response.audio_metadata,
            transcription_model=transcription_response.model,
            summary_model=summary_response.model,
        )

        st.session_state.latest_result = {
            "audio_path": str(audio_path),
            "audio_metadata": transcription_response.audio_metadata,
            "transcription_model": transcription_response.model,
            "summary_model": summary_response.model,
            "transcript": transcription_response.transcript,
            "summary": summary_response.summary,
            "saved_result": saved_result_path.name,
        }

        st.success(f"Analysis completed. Saved result: {saved_result_path.name}")

    except Exception as error:
        st.error(f"Failed to analyze audio: {error}")


def render_latest_result() -> None:
    """
    Render the latest audio analysis result.
    """
    result = st.session_state.latest_result

    if not result:
        return

    st.subheader("Transcript")
    render_text_with_direction(result["transcript"])

    st.subheader("Structured Summary")
    render_text_with_direction(result["summary"])

    with st.expander("Audio metadata"):
        render_audio_metadata(result["audio_metadata"])

    st.caption(f"Saved result: {result['saved_result']}")

    result_json = create_downloadable_result(result)

    st.download_button(
        label="Download Result JSON",
        data=result_json,
        file_name="audio_analysis_result.json",
        mime="application/json",
    )


def render_sidebar() -> None:
    """
    Render sidebar controls.
    """
    with st.sidebar:
        st.header("Audio Setup")

        uploaded_file = st.file_uploader(
            "Upload an audio file",
            type=["mp3", "wav", "m4a", "webm", "mp4"],
        )

        if uploaded_file is not None:
            audio_path = save_uploaded_audio(uploaded_file)

            if st.session_state.current_audio_name != uploaded_file.name:
                st.session_state.latest_result = None

            st.session_state.current_audio_path = audio_path
            st.session_state.current_audio_name = uploaded_file.name

            st.success(f"Audio saved: {audio_path.name}")

        st.divider()

        st.info(
            "Supported formats: MP3, WAV, M4A, WEBM, MP4. "
            "Use short audio files during testing to reduce cost and latency."
        )

        if st.button("Clear Current Result"):
            st.session_state.latest_result = None
            st.success("Current result cleared.")


def main() -> None:
    """
    Main Streamlit application.
    """
    ensure_directories()
    initialize_session_state()
    apply_custom_styles()

    st.title("AI Voice Meeting Assistant")
    st.caption(
        "Upload an audio file, transcribe it, and generate a structured "
        "summary with key points, action items, decisions, and open questions."
    )

    render_sidebar()

    if st.session_state.current_audio_path is None:
        st.info("Upload an audio file from the sidebar to start.")
        return

    audio_path = Path(st.session_state.current_audio_path)

    st.subheader("Uploaded Audio")
    st.audio(str(audio_path))

    loader = AudioLoader()
    loaded_audio = loader.load_audio(audio_path)
    render_audio_metadata(
        {
            "file_name": loaded_audio.file_name,
            "file_extension": loaded_audio.file_extension,
            "file_size_bytes": loaded_audio.file_size_bytes,
            "file_size_mb": loaded_audio.file_size_mb,
        }
    )

    if st.button("Analyze Audio"):
        analyze_audio(audio_path)

    render_latest_result()


if __name__ == "__main__":
    main()