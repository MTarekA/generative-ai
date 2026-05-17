from pathlib import Path

import streamlit as st
from PIL import Image

from app.config import (
    INTEGRATED_IMAGES_DIR,
    ensure_directories,
    get_settings,
)
from app.health_overview import (
    get_overall_portfolio_score,
    get_portfolio_health_overview,
)
from app.integrated_assistant import IntegratedWorkspaceAssistant
from app.integrated_vision_pipeline import IntegratedVisionPipeline
from app.integrated_workspace_manager import (
    INTEGRATED_WORKSPACE_DIR,
    IntegratedWorkspaceManager,
    ensure_integrated_workspace,
)
from app.project_registry import get_projects
from app.ui_components import (
    render_architecture_overview,
    render_capability_matrix,
    render_engineering_practices,
    render_footer,
    render_health_table,
    render_project_detail,
    render_projects_grid,
)


st.set_page_config(
    page_title="Multimodal AI Workspace",
    page_icon="🧠",
    layout="wide",
)


def apply_custom_styles() -> None:
    """
    Apply custom CSS styles for a cleaner Streamlit dashboard.
    """
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 3rem;
            padding-bottom: 5rem;
            max-width: 1250px;
        }

        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        [data-testid="stSidebar"] {
            background-color: #f7f9fc;
        }

        .hero-box {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border: 1px solid #e5e7eb;
            border-radius: 1.25rem;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .hero-text {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #374151;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.92rem;
        }

        .tool-box {
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 0.75rem;
            padding: 0.75rem;
            margin-top: 0.75rem;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """
    Render dashboard hero section.
    """
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">Multimodal AI Workspace</div>
            <div class="hero-text">
                A unified Generative AI portfolio dashboard bringing together
                document RAG, image understanding, audio transcription and
                summarization, and MCP-style workspace tools.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(project_names: list[str]) -> tuple[str, str]:
    """
    Render sidebar navigation and return selected page and selected project.
    """
    with st.sidebar:
        st.header("Navigation")

        page = st.radio(
            "Choose a section",
            options=[
                "Overview",
                "Projects",
                "Capability Matrix",
                "Health Overview",
                "Architecture",
                "Project Details",
                "Integrated Demo",
            ],
        )

        st.divider()

        st.subheader("Project Details")

        selected_project = st.selectbox(
            "Select project",
            options=project_names,
        )

        st.divider()

        st.caption(
            "This hub is designed as a portfolio-level control center. "
            "Each individual project remains independently runnable."
        )

    return page, selected_project


def render_overview_page() -> None:
    """
    Render portfolio overview page.
    """
    projects = get_projects()
    health_score = get_overall_portfolio_score()

    render_hero()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Projects", len(projects))

    with col2:
        st.metric(
            "Completed",
            len([p for p in projects if p.status == "Completed"]),
        )

    with col3:
        st.metric("AI Areas", len(set(project.area for project in projects)))

    with col4:
        st.metric(
            "Readiness",
            f"{int(health_score['readiness_score'] * 100)}%",
        )

    st.subheader("Portfolio Projects")
    render_projects_grid(projects)

    st.subheader("Engineering Focus")
    render_engineering_practices()


def render_projects_page() -> None:
    """
    Render all project cards.
    """
    st.title("Projects")
    st.caption(
        "Four practical Generative AI projects covering text, vision, audio, "
        "and tool-connected assistants."
    )

    render_projects_grid(get_projects())


def render_capability_page() -> None:
    """
    Render capability matrix page.
    """
    st.title("Capability Matrix")
    st.caption(
        "A compact overview of the main capabilities demonstrated across "
        "the portfolio."
    )

    render_capability_matrix(get_projects())


def render_health_page() -> None:
    """
    Render health overview page.
    """
    st.title("Portfolio Health Overview")
    st.caption(
        "A system-level check showing whether each project includes the "
        "expected structure, documentation, UI, tests, and screenshots."
    )

    statuses = get_portfolio_health_overview()
    score = get_overall_portfolio_score()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Projects", score["total_projects"])

    with col2:
        st.metric(
            "Checks Passed",
            f"{score['total_passed_checks']}/{score['total_possible_checks']}",
        )

    with col3:
        st.metric(
            "Readiness Score",
            f"{int(score['readiness_score'] * 100)}%",
        )

    render_health_table(statuses)


def render_architecture_page() -> None:
    """
    Render architecture overview page.
    """
    st.title("Architecture Overview")
    st.caption(
        "A high-level view of how the individual projects are structured "
        "and what AI workflow each one demonstrates."
    )

    render_architecture_overview()

    st.subheader("Why this structure matters")
    st.write(
        "The portfolio separates each AI capability into an independently "
        "runnable project while also providing this unified dashboard as a "
        "system-level overview. This keeps the codebase modular, easier to "
        "debug, and easier to extend."
    )


def render_project_details_page(selected_project_name: str) -> None:
    """
    Render details for one selected project.
    """
    projects = get_projects()

    selected_project = next(
        project
        for project in projects
        if project.name == selected_project_name
    )

    render_project_detail(selected_project)


def initialize_integrated_workspace_state() -> None:
    """
    Initialize session state for the integrated workspace tools demo.
    """
    if "integrated_workspace_messages" not in st.session_state:
        st.session_state.integrated_workspace_messages = []

    if "integrated_workspace_assistant" not in st.session_state:
        st.session_state.integrated_workspace_assistant = (
            IntegratedWorkspaceAssistant()
        )


def render_integrated_workspace_files() -> None:
    """
    Render files currently available in the integrated workspace.
    """
    manager = IntegratedWorkspaceManager()
    files = manager.list_files()

    st.subheader("Integrated Workspace Files")

    if not files:
        st.info("No files found in the integrated workspace.")
        return

    for file in files:
        st.write(f"- {file.relative_path}")


def render_integrated_tool_result(tool_name: str, tool_result) -> None:
    """
    Render structured tool result for the integrated workspace assistant.
    """
    with st.expander("Tool details"):
        st.markdown(
            f'<div class="tool-box">Tool used: <code>{tool_name}</code></div>',
            unsafe_allow_html=True,
        )

        if tool_result is None:
            st.info("No structured tool result returned.")
        else:
            st.json(tool_result)


def render_integrated_workspace_chat_history() -> None:
    """
    Render integrated workspace chat history.
    """
    for message in st.session_state.integrated_workspace_messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            st.write(content)

            if role == "assistant":
                render_integrated_tool_result(
                    tool_name=message.get("tool_name", "none"),
                    tool_result=message.get("tool_result"),
                )


def handle_integrated_workspace_message(user_message: str) -> None:
    """
    Process a user message through the integrated workspace assistant.
    """
    st.session_state.integrated_workspace_messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.write(user_message)

    with st.chat_message("assistant"):
        try:
            response = (
                st.session_state.integrated_workspace_assistant
                .handle_message(user_message)
            )

            st.write(response.message)

            render_integrated_tool_result(
                tool_name=response.tool_name,
                tool_result=response.tool_result,
            )

            st.session_state.integrated_workspace_messages.append(
                {
                    "role": "assistant",
                    "content": response.message,
                    "tool_name": response.tool_name,
                    "tool_result": response.tool_result,
                }
            )

        except Exception as error:
            error_message = f"Error: {error}"
            st.error(error_message)

            st.session_state.integrated_workspace_messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "tool_name": "error",
                    "tool_result": None,
                }
            )


def render_workspace_tools_integrated_tab() -> None:
    """
    Render the fully integrated MCP-style workspace tools tab.
    """
    ensure_integrated_workspace()
    initialize_integrated_workspace_state()

    st.subheader("Workspace Tools")
    st.write(
        "This tab is the first fully integrated capability inside the "
        "Multimodal AI Workspace. It provides safe local file interaction "
        "through MCP-style tools."
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            Try commands like:

            ```text
            help
            list files
            write note demo | This note was created inside the integrated workspace.
            read notes/demo.md
            search integrated
            create task demo_tasks | Demo Tasks | Test chat; Check files; Export results
            ```
            """
        )

    with col2:
        st.caption("All file operations are restricted to:")
        st.code(str(INTEGRATED_WORKSPACE_DIR), language="text")

    st.divider()

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Integrated Workspace Chat")

        render_integrated_workspace_chat_history()

        user_message = st.chat_input(
            "Type a workspace command, for example: list files"
        )

        if user_message:
            handle_integrated_workspace_message(user_message)

    with right_col:
        render_integrated_workspace_files()

        st.divider()

        if st.button("Refresh Integrated Workspace"):
            st.rerun()

        if st.button("Clear Integrated Chat History"):
            st.session_state.integrated_workspace_messages = []
            st.success("Integrated workspace chat history cleared.")


def initialize_integrated_vision_state() -> None:
    """
    Initialize session state for the integrated vision demo.
    """
    if "integrated_vision_messages" not in st.session_state:
        st.session_state.integrated_vision_messages = []

    if "integrated_current_image_path" not in st.session_state:
        st.session_state.integrated_current_image_path = None

    if "integrated_current_image_name" not in st.session_state:
        st.session_state.integrated_current_image_name = None


def save_integrated_uploaded_image(uploaded_file) -> Path:
    """
    Save uploaded image into integrated_uploads/images.
    """
    INTEGRATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    file_path = INTEGRATED_IMAGES_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def render_integrated_image_metadata(metadata: dict) -> None:
    """
    Render image metadata in a compact format.
    """
    with st.expander("Image metadata"):
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


def render_integrated_vision_history() -> None:
    """
    Render previous integrated vision questions and answers.
    """
    for message in st.session_state.integrated_vision_messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            st.write(content)

            if role == "assistant" and message.get("image_metadata"):
                render_integrated_image_metadata(message["image_metadata"])


def handle_integrated_vision_question(
    image_path: Path,
    question: str,
) -> None:
    """
    Analyze an image question through the integrated vision pipeline.
    """
    st.session_state.integrated_vision_messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Analyzing image..."):
                pipeline = IntegratedVisionPipeline()
                response = pipeline.analyze_image(
                    image_path=image_path,
                    question=question,
                )

            st.write(response.answer)

            render_integrated_image_metadata(response.image_metadata)

            st.session_state.integrated_vision_messages.append(
                {
                    "role": "assistant",
                    "content": response.answer,
                    "image_metadata": response.image_metadata,
                    "question": response.question,
                    "model": response.model,
                }
            )

        except Exception as error:
            error_message = f"Error: {error}"
            st.error(error_message)

            st.session_state.integrated_vision_messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "image_metadata": {},
                }
            )


def render_image_understanding_integrated_tab() -> None:
    """
    Render the integrated image understanding tab.
    """
    initialize_integrated_vision_state()

    st.subheader("Image Understanding")
    st.write(
        "This tab integrates image upload and vision-language analysis "
        "directly inside the Multimodal AI Workspace."
    )

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
        key="integrated_vision_uploader",
    )

    if uploaded_file is not None:
        image_path = save_integrated_uploaded_image(uploaded_file)

        if st.session_state.integrated_current_image_name != uploaded_file.name:
            st.session_state.integrated_vision_messages = []

        st.session_state.integrated_current_image_path = image_path
        st.session_state.integrated_current_image_name = uploaded_file.name

        st.success(f"Image saved: {image_path.name}")

    if st.session_state.integrated_current_image_path is None:
        st.info("Upload an image to start the integrated vision demo.")
        return

    image_path = Path(st.session_state.integrated_current_image_path)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Uploaded Image")
        image = Image.open(image_path)
        st.image(
            image,
            caption=st.session_state.integrated_current_image_name,
            use_container_width=True,
        )

    with right_col:
        st.subheader("Chat with the image")

        st.caption(
            "Example questions: "
            "Describe this image. / What text is visible? / اشرح الصورة دي."
        )

        render_integrated_vision_history()

        question = st.chat_input(
            "Ask a question about the uploaded image...",
            key="integrated_vision_chat_input",
        )

        if question:
            handle_integrated_vision_question(
                image_path=image_path,
                question=question,
            )

    st.divider()

    if st.button("Clear Integrated Vision History"):
        st.session_state.integrated_vision_messages = []
        st.success("Integrated vision history cleared.")


def render_integrated_demo_page() -> None:
    """
    Render the integrated demo page.

    This page is the starting point for phase two of the portfolio:
    a single interface that will gradually integrate the actual
    functionality of the four individual projects.
    """
    st.title("Integrated Multimodal Demo")
    st.caption(
        "Phase two of the portfolio: a unified workspace where document RAG, "
        "image understanding, audio summarization, and MCP-style tools will "
        "become accessible from one interface."
    )

    st.info(
        "This section is being built incrementally. "
        "The Workspace Tools tab is already integrated locally, and the "
        "Image Understanding tab is now integrated with an OpenAI vision model."
    )

    rag_tab, vision_tab, audio_tab, mcp_tab = st.tabs(
        [
            "Document RAG",
            "Image Understanding",
            "Audio Summary",
            "Workspace Tools",
        ]
    )

    with rag_tab:
        st.subheader("Document RAG")
        st.write(
            "This tab will integrate the document question-answering workflow "
            "from the AI Study Assistant project."
        )

        st.markdown(
            """
            Planned capabilities:

            - Upload PDF or TXT files
            - Build or load a local knowledge base
            - Ask questions grounded in uploaded documents
            - Show retrieved source previews
            - Export chat history
            """
        )

        st.warning(
            "Status: planned integration. "
            "This will be added after the lighter integrations are stable."
        )

    with vision_tab:
        render_image_understanding_integrated_tab()

    with audio_tab:
        st.subheader("Audio Summary")
        st.write(
            "This tab will integrate audio transcription and structured "
            "summarization from the AI Voice Meeting Assistant project."
        )

        st.markdown(
            """
            Planned capabilities:

            - Upload MP3, WAV, M4A, WEBM, or MP4 files
            - Transcribe speech to text
            - Generate structured summaries
            - Extract action items, decisions, and open questions
            - Save and export results
            """
        )

        st.warning(
            "Status: planned integration. "
            "This will be added after the vision integration."
        )

    with mcp_tab:
        render_workspace_tools_integrated_tab()

    st.divider()

    st.subheader("Integration Roadmap")

    st.code(
        """
Phase 2 Integration Roadmap

1. Integrated Demo page structure
2. MCP Workspace Tools tab
3. Vision Image Understanding tab
4. Audio Transcription and Summary tab
5. Document RAG tab
6. Shared UX and export layer
7. Tests, health checks, README update, screenshots
        """,
        language="text",
    )


def main() -> None:
    """
    Main Streamlit dashboard.
    """
    ensure_directories()
    apply_custom_styles()

    settings = get_settings()
    projects = get_projects()
    project_names = [project.name for project in projects]

    page, selected_project = render_sidebar(project_names)

    if page == "Overview":
        render_overview_page()

    elif page == "Projects":
        render_projects_page()

    elif page == "Capability Matrix":
        render_capability_page()

    elif page == "Health Overview":
        render_health_page()

    elif page == "Architecture":
        render_architecture_page()

    elif page == "Project Details":
        render_project_details_page(selected_project)

    elif page == "Integrated Demo":
        render_integrated_demo_page()

    render_footer()


if __name__ == "__main__":
    main()