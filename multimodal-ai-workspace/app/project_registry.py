from dataclasses import dataclass
from pathlib import Path

from app.config import PORTFOLIO_ROOT


@dataclass(frozen=True)
class PortfolioProject:
    """
    Structured metadata for a portfolio project.
    """

    name: str
    folder_name: str
    area: str
    status: str
    description: str
    local_path: Path
    streamlit_command: str
    test_command: str
    health_check_command: str
    key_features: list[str]
    screenshots: list[str]


def get_projects() -> list[PortfolioProject]:
    """
    Return all Generative AI portfolio projects.
    """
    return [
        PortfolioProject(
            name="AI Study Assistant",
            folder_name="ai-study-assistant",
            area="RAG / Text",
            status="Completed",
            description=(
                "A Retrieval-Augmented Generation application for asking "
                "questions about uploaded lecture documents."
            ),
            local_path=PORTFOLIO_ROOT / "ai-study-assistant",
            streamlit_command=(
                "cd ai-study-assistant && "
                "python -m streamlit run streamlit_app.py"
            ),
            test_command="cd ai-study-assistant && python -m pytest",
            health_check_command="cd ai-study-assistant && python health_check.py",
            key_features=[
                "PDF/TXT document upload",
                "FAISS vector store",
                "RAG-based question answering",
                "Source previews",
                "Arabic RTL support",
                "Evaluation script",
                "Unit tests and health check",
            ],
            screenshots=[
                "ai-study-assistant/assets/screenshot.png",
            ],
        ),
        PortfolioProject(
            name="AI Image Understanding Assistant",
            folder_name="vision-image-analyzer",
            area="Vision",
            status="Completed",
            description=(
                "A vision-language application for analyzing uploaded images "
                "and answering questions about their visual content."
            ),
            local_path=PORTFOLIO_ROOT / "vision-image-analyzer",
            streamlit_command=(
                "cd vision-image-analyzer && "
                "python -m streamlit run streamlit_app.py"
            ),
            test_command="cd vision-image-analyzer && python -m pytest",
            health_check_command=(
                "cd vision-image-analyzer && python health_check.py"
            ),
            key_features=[
                "Image upload and validation",
                "Vision model analysis",
                "Image question answering",
                "Chat-style UI",
                "Result saving as JSON",
                "Arabic RTL support",
                "Unit tests and health check",
            ],
            screenshots=[
                "vision-image-analyzer/assets/screenshot_upload_transcript.png",
                "vision-image-analyzer/assets/screenshot_summary_result.png",
                "vision-image-analyzer/assets/screenshot.png",
            ],
        ),
        PortfolioProject(
            name="AI Voice Meeting Assistant",
            folder_name="voice-meeting-assistant",
            area="Voice / Audio",
            status="Completed",
            description=(
                "A voice/audio application for transcribing audio files and "
                "generating structured summaries."
            ),
            local_path=PORTFOLIO_ROOT / "voice-meeting-assistant",
            streamlit_command=(
                "cd voice-meeting-assistant && "
                "python -m streamlit run streamlit_app.py"
            ),
            test_command="cd voice-meeting-assistant && python -m pytest",
            health_check_command=(
                "cd voice-meeting-assistant && python health_check.py"
            ),
            key_features=[
                "Audio upload",
                "Speech-to-text transcription",
                "Transcript summarization",
                "Structured meeting notes",
                "JSON result export",
                "Logging",
                "Unit tests and health check",
            ],
            screenshots=[
                "voice-meeting-assistant/assets/screenshot_upload_transcript.png",
                "voice-meeting-assistant/assets/screenshot_summary_result.png",
                "voice-meeting-assistant/assets/screenshot.png",
            ],
        ),
        PortfolioProject(
            name="MCP Workspace Assistant",
            folder_name="mcp-workspace-assistant",
            area="MCP / Tools",
            status="Completed",
            description=(
                "A tool-connected workspace assistant for safely interacting "
                "with local files through MCP-style tools."
            ),
            local_path=PORTFOLIO_ROOT / "mcp-workspace-assistant",
            streamlit_command=(
                "cd mcp-workspace-assistant && "
                "python -m streamlit run streamlit_app.py"
            ),
            test_command="cd mcp-workspace-assistant && python -m pytest",
            health_check_command=(
                "cd mcp-workspace-assistant && python health_check.py"
            ),
            key_features=[
                "Safe workspace file access",
                "MCP-style tools",
                "Note creation",
                "Task file generation",
                "Workspace search",
                "Path traversal protection",
                "Unit tests and health check",
            ],
            screenshots=[
                "mcp-workspace-assistant/assets/screenshot_chat_commands.png",
                "mcp-workspace-assistant/assets/screenshot_workspace_tools.png",
                "mcp-workspace-assistant/assets/screenshot_task_creation.png",
            ],
        ),
    ]


def get_project_by_folder_name(folder_name: str) -> PortfolioProject | None:
    """
    Return a project by folder name.
    """
    for project in get_projects():
        if project.folder_name == folder_name:
            return project

    return None


def get_completed_projects() -> list[PortfolioProject]:
    """
    Return completed projects.
    """
    return [
        project
        for project in get_projects()
        if project.status.lower() == "completed"
    ]


def get_project_count_by_area() -> dict[str, int]:
    """
    Return the number of projects per area.
    """
    counts: dict[str, int] = {}

    for project in get_projects():
        counts[project.area] = counts.get(project.area, 0) + 1

    return counts


if __name__ == "__main__":
    for project in get_projects():
        print("=" * 80)
        print(project.name)
        print("Area:", project.area)
        print("Status:", project.status)
        print("Path:", project.local_path)
        print("Exists:", project.local_path.exists())