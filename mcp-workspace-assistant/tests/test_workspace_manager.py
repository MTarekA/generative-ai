from pathlib import Path

import pytest

from app.workspace_manager import WorkspaceManager


def test_workspace_manager_writes_and_reads_text_file(
    tmp_path: Path,
) -> None:
    """
    Test safe writing and reading inside the workspace.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)

    manager.write_text_file(
        relative_path="notes/test_note.md",
        content="This is a test note.",
        overwrite=True,
    )

    content = manager.read_text_file("notes/test_note.md")

    assert content == "This is a test note."


def test_workspace_manager_lists_files(tmp_path: Path) -> None:
    """
    Test listing files inside the workspace.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)

    manager.write_text_file(
        relative_path="notes/a.md",
        content="A",
        overwrite=True,
    )
    manager.write_text_file(
        relative_path="tasks/b.md",
        content="B",
        overwrite=True,
    )

    files = manager.list_files()
    relative_paths = [file.relative_path for file in files]

    assert "notes\\a.md" in relative_paths or "notes/a.md" in relative_paths
    assert "tasks\\b.md" in relative_paths or "tasks/b.md" in relative_paths


def test_workspace_manager_blocks_path_traversal(tmp_path: Path) -> None:
    """
    Test that unsafe paths outside the workspace are blocked.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)

    with pytest.raises(ValueError, match="Unsafe path access blocked"):
        manager.read_text_file("../../secret.txt")


def test_workspace_manager_searches_text_files(tmp_path: Path) -> None:
    """
    Test searching inside workspace text files.
    """
    manager = WorkspaceManager(workspace_dir=tmp_path)

    manager.write_text_file(
        relative_path="notes/search_test.md",
        content="This file contains the keyword Streamlit.",
        overwrite=True,
    )

    results = manager.search_text_files("Streamlit")

    assert len(results) == 1
    assert results[0]["file_name"] == "search_test.md"
    assert "Streamlit" in results[0]["snippet"]