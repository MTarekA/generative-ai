import json

import streamlit as st

from app.assistant_pipeline import AssistantPipeline
from app.config import WORKSPACE_DIR, ensure_directories
from app.workspace_manager import WorkspaceManager


st.set_page_config(
    page_title="MCP Workspace Assistant",
    page_icon="🛠️",
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

        .tool-box {
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 0.75rem;
            padding: 0.75rem;
            margin-top: 0.75rem;
            font-size: 0.95rem;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.9rem;
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

    if "assistant" not in st.session_state:
        st.session_state.assistant = AssistantPipeline()


def export_chat_history() -> str:
    """
    Export the current chat history as JSON.
    """
    export_data = {
        "app": "MCP Workspace Assistant",
        "workspace_dir": str(WORKSPACE_DIR),
        "messages": st.session_state.messages,
    }

    return json.dumps(
        export_data,
        ensure_ascii=False,
        indent=2,
    )


def render_command_examples() -> None:
    """
    Render supported command examples.
    """
    st.markdown(
        """
        Try commands like:

        ```text
        help
        list files
        write note project_idea | This is my project idea.
        append note project_idea | More details about the idea.
        read notes/project_idea.md
        search project
        create task next_steps | Next Steps | Build UI; Add tests; Write README
        ```
        """
    )


def render_workspace_files() -> None:
    """
    Render current workspace files in the sidebar.
    """
    manager = WorkspaceManager()
    files = manager.list_files()

    st.subheader("Workspace Files")

    if not files:
        st.info("No files found in workspace.")
        return

    for file in files:
        st.write(f"- {file.relative_path}")


def render_tool_result(tool_name: str, tool_result) -> None:
    """
    Render raw tool result inside an expandable section.
    """
    with st.expander("Tool details"):
        st.markdown(
            f'<div class="tool-box">Tool used: {tool_name}</div>',
            unsafe_allow_html=True,
        )

        if tool_result is None:
            st.info("No structured tool result returned.")
        else:
            st.json(tool_result)


def render_chat_history() -> None:
    """
    Render previous user and assistant messages.
    """
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            render_text_with_direction(content)

            if role == "assistant":
                render_tool_result(
                    tool_name=message.get("tool_name", "none"),
                    tool_result=message.get("tool_result"),
                )


def handle_user_message(user_message: str) -> None:
    """
    Process a user command through the assistant pipeline.
    """
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        render_text_with_direction(user_message)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.assistant.handle_message(user_message)

            render_text_with_direction(response.message)

            render_tool_result(
                tool_name=response.tool_name,
                tool_result=response.tool_result,
            )

            st.session_state.messages.append(
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

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "tool_name": "error",
                    "tool_result": None,
                }
            )


def render_sidebar() -> None:
    """
    Render sidebar controls and workspace overview.
    """
    with st.sidebar:
        st.header("Workspace Setup")

        st.caption("All file operations are restricted to:")

        st.code(str(WORKSPACE_DIR), language="text")

        st.divider()

        render_workspace_files()

        st.divider()

        if st.button("Refresh Workspace View"):
            st.rerun()

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared.")

        if st.session_state.messages:
            chat_json = export_chat_history()

            st.download_button(
                label="Download Chat History",
                data=chat_json,
                file_name="mcp_workspace_chat_history.json",
                mime="application/json",
            )


def main() -> None:
    """
    Main Streamlit application.
    """
    ensure_directories()
    initialize_session_state()
    apply_custom_styles()

    st.title("MCP Workspace Assistant")
    st.caption(
        "A tool-connected AI assistant for safely interacting with a local "
        "workspace through MCP-style tools."
    )

    render_sidebar()

    chat_tab, commands_tab = st.tabs(["Chat", "Commands"])

    with chat_tab:
        st.subheader("Chat with your workspace tools")

        render_chat_history()

        user_message = st.chat_input(
            "Type a command, for example: list files"
        )

        if user_message:
            handle_user_message(user_message)

    with commands_tab:
        st.subheader("Supported Commands")
        render_command_examples()


if __name__ == "__main__":
    main()