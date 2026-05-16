from pathlib import Path

from app.tools import WorkspaceTools
from app.workspace_manager import WorkspaceManager


def test_workspace_tools_write_and_read_note(tmp_path: Path) -> None:
    """
    Test writing and reading a workspace note through tools.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)
    tools = WorkspaceTools(manager=manager)

    write_result = tools.write_workspace_note(
        file_name="tool_note",
        content="This note was created by a tool.",
        overwrite=True,
    )

    assert write_result["status"] == "success"
    assert write_result["relative_path"].endswith("tool_note.md")

    read_result = tools.read_workspace_file("notes/tool_note.md")

    assert "created by a tool" in read_result["content"]


def test_workspace_tools_create_task_file(tmp_path: Path) -> None:
    """
    Test creating a task file through tools.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)
    tools = WorkspaceTools(manager=manager)

    result = tools.create_task_file(
        file_name="tool_tasks",
        title="Tool Tasks",
        tasks=["Build tools", "Add tests"],
        overwrite=True,
    )

    assert result["status"] == "success"
    assert result["task_count"] == 2

    content = manager.read_text_file("tasks/tool_tasks.md")

    assert "# Tool Tasks" in content
    assert "- [ ] Build tools" in content
    assert "- [ ] Add tests" in content


def test_workspace_tools_search_workspace(tmp_path: Path) -> None:
    """
    Test searching workspace files through tools.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)
    tools = WorkspaceTools(manager=manager)

    tools.write_workspace_note(
        file_name="search_note",
        content="This note contains MCP architecture details.",
        overwrite=True,
    )

    results = tools.search_workspace("MCP")

    assert len(results) == 1
    assert results[0]["file_name"] == "search_note.md"