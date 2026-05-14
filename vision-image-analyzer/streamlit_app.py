import json
from pathlib import Path

import streamlit as st
from PIL import Image

from app.config import UPLOADED_IMAGES_DIR, ensure_directories
from app.result_manager import ResultManager
from app.vision_pipeline import VisionPipeline


st.set_page_config(
    page_title="AI Image Understanding Assistant",
    page_icon="🖼️",
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

        [data-testid="stChatMessage"] p {
            line-height: 1.8;
            font-size: 1rem;
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
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_image_path" not in st.session_state:
        st.session_state.current_image_path = None

    if "current_image_name" not in st.session_state:
        st.session_state.current_image_name = None


def save_uploaded_image(uploaded_file) -> Path:
    """
    Save an uploaded image to the uploaded images directory.
    """
    ensure_directories()

    file_path = UPLOADED_IMAGES_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def export_analysis_history() -> str:
    """
    Export the current image analysis chat history as JSON.
    """
    export_data = {
        "app": "AI Image Understanding Assistant",
        "image_name": st.session_state.current_image_name,
        "image_path": str(st.session_state.current_image_path),
        "messages": st.session_state.messages,
    }

    return json.dumps(
        export_data,
        ensure_ascii=False,
        indent=2,
    )


def render_image_metadata(metadata: dict) -> None:
    """
    Render image metadata in a readable format.
    """
    st.markdown('<div class="metadata-box">', unsafe_allow_html=True)

    st.subheader("Image Metadata")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Width", metadata.get("width", "N/A"))

    with col2:
        st.metric("Height", metadata.get("height", "N/A"))

    with col3:
        st.metric("Mode", metadata.get("mode", "N/A"))

    st.write(f"File name: {metadata.get('file_name', 'unknown')}")
    st.write(f"File type: {metadata.get('file_extension', 'unknown')}")
    st.write(f"MIME type: {metadata.get('mime_type', 'unknown')}")

    st.markdown("</div>", unsafe_allow_html=True)


def render_chat_history() -> None:
    """
    Render previous questions and answers.
    """
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            render_text_with_direction(content)

            if role == "assistant" and message.get("image_metadata"):
                with st.expander("Image metadata"):
                    render_image_metadata(message["image_metadata"])

            if role == "assistant" and message.get("saved_result"):
                st.caption(f"Saved result: {message['saved_result']}")


def analyze_user_question(image_path: Path, question: str) -> None:
    """
    Analyze the current image with the user's question.
    """
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        render_text_with_direction(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Analyzing image..."):
                pipeline = VisionPipeline()
                response = pipeline.analyze_image(
                    image_path=image_path,
                    question=question,
                )

            render_text_with_direction(response.answer)

            result_manager = ResultManager()
            saved_result_path = result_manager.save_analysis_result(
                image_path=image_path,
                question=response.question,
                answer=response.answer,
                image_metadata=response.image_metadata,
            )

            st.caption(f"Saved result: {saved_result_path.name}")

            with st.expander("Image metadata"):
                render_image_metadata(response.image_metadata)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.answer,
                    "image_metadata": response.image_metadata,
                    "question": response.question,
                    "saved_result": saved_result_path.name,
                }
            )

        except Exception as error:
            error_message = f"Failed to analyze image: {error}"
            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "image_metadata": {},
                }
            )


def render_sidebar() -> None:
    """
    Render sidebar controls.
    """
    with st.sidebar:
        st.header("Image Setup")

        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
        )

        if uploaded_file is not None:
            image_path = save_uploaded_image(uploaded_file)

            if st.session_state.current_image_name != uploaded_file.name:
                st.session_state.messages = []

            st.session_state.current_image_path = image_path
            st.session_state.current_image_name = uploaded_file.name

            st.success(f"Image saved: {image_path.name}")

        st.divider()

        st.info(
            "Supported formats: PNG, JPG, JPEG, WEBP. "
            "Use clear images for better analysis."
        )

        if st.button("Clear Analysis History"):
            st.session_state.messages = []
            st.success("Analysis history cleared.")

        if st.session_state.messages:
            analysis_json = export_analysis_history()

            st.download_button(
                label="Download Analysis History",
                data=analysis_json,
                file_name="image_analysis_history.json",
                mime="application/json",
            )


def main() -> None:
    """
    Main Streamlit application.
    """
    ensure_directories()
    initialize_session_state()
    apply_custom_styles()

    st.title("AI Image Understanding Assistant")
    st.caption(
        "Upload an image and ask questions about its visual content "
        "using a vision-capable language model."
    )

    render_sidebar()

    if st.session_state.current_image_path is None:
        st.info("Upload an image from the sidebar to start.")
        return

    image_path = Path(st.session_state.current_image_path)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Uploaded Image")
        image = Image.open(image_path)
        st.image(
            image,
            caption=st.session_state.current_image_name,
            use_container_width=True,
        )

    with right_col:
        st.subheader("Chat with the image")

        render_chat_history()

        question = st.chat_input(
            "Ask a question about the image..."
        )

        if question:
            analyze_user_question(
                image_path=image_path,
                question=question,
            )


if __name__ == "__main__":
    main()