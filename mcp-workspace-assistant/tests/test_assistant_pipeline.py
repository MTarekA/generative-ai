from pathlib import Path

from app.assistant_pipeline import AssistantPipeline
from app.tools import WorkspaceTools
from app.workspace_manager import WorkspaceManager


def create_test_assistant(tmp_path: Path) -> AssistantPipeline:
    """
    Create an assistant with an isolated temporary workspace.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)
    tools = WorkspaceTools(manager=manager)
    return AssistantPipeline(tools=tools)


def test_assistant_returns_help(tmp_path: Path) -> None:
    """
    Test help command.
    """
    assistant = create_test_assistant(tmp_path)

    response = assistant.handle_message("help")

    assert response.tool_name == "help"
    assert "Supported commands" in response.message


def test_assistant_writes_and_reads_note(tmp_path: Path) -> None:
    """
    Test writing and reading a note through assistant commands.
    """
    assistant = create_test_assistant(tmp_path)

    write_response = assistant.handle_message(
        "write note idea | This is my idea."
    )

    assert write_response.tool_name == "write_workspace_note"

    read_response = assistant.handle_message("read notes/idea.md")

    assert read_response.tool_name == "read_workspace_file"
    assert "This is my idea." in read_response.message


def test_assistant_searches_workspace(tmp_path: Path) -> None:
    """
    Test search command through assistant.
    """
    assistant = create_test_assistant(tmp_path)

    assistant.handle_message(
        "write note search_demo | This note mentions Streamlit."
    )

    response = assistant.handle_message("search Streamlit")

    assert response.tool_name == "search_workspace"
    assert "search_demo.md" in response.message


def test_assistant_creates_task_file(tmp_path: Path) -> None:
    """
    Test create task command.
    """
    assistant = create_test_assistant(tmp_path)

    response = assistant.handle_message(
        "create task next | Next Tasks | Build UI; Add tests"
    )

    assert response.tool_name == "create_task_file"
    assert "2 tasks" in response.message