from pathlib import Path

import pytest

from app.integrated_assistant import IntegratedWorkspaceAssistant
from app.integrated_workspace_manager import IntegratedWorkspaceManager
from app.integrated_workspace_tools import IntegratedWorkspaceTools


def create_test_assistant(tmp_path: Path) -> IntegratedWorkspaceAssistant:
    """
    Create an integrated assistant with an isolated temporary workspace.
    """
    manager = IntegratedWorkspaceManager(workspace_dir=tmp_path)
    tools = IntegratedWorkspaceTools(manager=manager)
    return IntegratedWorkspaceAssistant(tools=tools)


def test_integrated_workspace_manager_writes_and_reads_file(
    tmp_path: Path,
) -> None:
    """
    Test safe writing and reading inside the integrated workspace.
    """
    manager = IntegratedWorkspaceManager(workspace_dir=tmp_path)

    manager.write_text_file(
        relative_path="notes/test_note.md",
        content="This is an integrated test note.",
        overwrite=True,
    )

    content = manager.read_text_file("notes/test_note.md")

    assert content == "This is an integrated test note."


def test_integrated_workspace_manager_blocks_path_traversal(
    tmp_path: Path,
) -> None:
    """
    Test that unsafe paths outside the integrated workspace are blocked.
    """
    manager = IntegratedWorkspaceManager(workspace_dir=tmp_path)

    with pytest.raises(ValueError, match="Unsafe path access blocked"):
        manager.read_text_file("../../secret.txt")


def test_integrated_workspace_tools_create_note(
    tmp_path: Path,
) -> None:
    """
    Test creating a note through integrated workspace tools.
    """
    manager = IntegratedWorkspaceManager(workspace_dir=tmp_path)
    tools = IntegratedWorkspaceTools(manager=manager)

    result = tools.write_workspace_note(
        file_name="tool_note",
        content="This note was created by integrated tools.",
        overwrite=True,
    )

    assert result["status"] == "success"
    assert result["relative_path"].endswith("tool_note.md")

    read_result = tools.read_workspace_file("notes/tool_note.md")

    assert "integrated tools" in read_result["content"]


def test_integrated_workspace_tools_create_task_file(
    tmp_path: Path,
) -> None:
    """
    Test creating a task file through integrated workspace tools.
    """
    manager = IntegratedWorkspaceManager(workspace_dir=tmp_path)
    tools = IntegratedWorkspaceTools(manager=manager)

    result = tools.create_task_file(
        file_name="tool_tasks",
        title="Integrated Tool Tasks",
        tasks=["Build MCP tab", "Add tests"],
        overwrite=True,
    )

    assert result["status"] == "success"
    assert result["task_count"] == 2

    content = manager.read_text_file("tasks/tool_tasks.md")

    assert "# Integrated Tool Tasks" in content
    assert "- [ ] Build MCP tab" in content
    assert "- [ ] Add tests" in content


def test_integrated_assistant_returns_help(tmp_path: Path) -> None:
    """
    Test help command in the integrated assistant.
    """
    assistant = create_test_assistant(tmp_path)

    response = assistant.handle_message("help")

    assert response.tool_name == "help"
    assert "Supported commands" in response.message


def test_integrated_assistant_writes_and_reads_note(
    tmp_path: Path,
) -> None:
    """
    Test writing and reading a note through integrated assistant commands.
    """
    assistant = create_test_assistant(tmp_path)

    write_response = assistant.handle_message(
        "write note idea | This is my integrated idea."
    )

    assert write_response.tool_name == "write_workspace_note"

    read_response = assistant.handle_message("read notes/idea.md")

    assert read_response.tool_name == "read_workspace_file"
    assert "This is my integrated idea." in read_response.message


def test_integrated_assistant_searches_workspace(
    tmp_path: Path,
) -> None:
    """
    Test search command through the integrated assistant.
    """
    assistant = create_test_assistant(tmp_path)

    assistant.handle_message(
        "write note search_demo | This note mentions multimodal integration."
    )

    response = assistant.handle_message("search multimodal")

    assert response.tool_name == "search_workspace"
    assert "search_demo.md" in response.message


def test_integrated_assistant_creates_task_file(
    tmp_path: Path,
) -> None:
    """
    Test task creation through the integrated assistant.
    """
    assistant = create_test_assistant(tmp_path)

    response = assistant.handle_message(
        "create task next | Next Tasks | Build UI; Add tests"
    )

    assert response.tool_name == "create_task_file"
    assert "2 tasks" in response.message