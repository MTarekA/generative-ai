from app.project_registry import (
    get_completed_projects,
    get_project_by_folder_name,
    get_project_count_by_area,
    get_projects,
)


def test_get_projects_returns_four_projects() -> None:
    """
    Test that the portfolio registry contains the four core projects.
    """
    projects = get_projects()

    assert len(projects) == 4


def test_all_projects_are_completed() -> None:
    """
    Test that all registered portfolio projects are completed.
    """
    completed_projects = get_completed_projects()

    assert len(completed_projects) == 4


def test_get_project_by_folder_name() -> None:
    """
    Test retrieving a project by folder name.
    """
    project = get_project_by_folder_name("ai-study-assistant")

    assert project is not None
    assert project.name == "AI Study Assistant"
    assert project.area == "RAG / Text"


def test_project_count_by_area() -> None:
    """
    Test project counts by area.
    """
    counts = get_project_count_by_area()

    assert counts["RAG / Text"] == 1
    assert counts["Vision"] == 1
    assert counts["Voice / Audio"] == 1
    assert counts["MCP / Tools"] == 1