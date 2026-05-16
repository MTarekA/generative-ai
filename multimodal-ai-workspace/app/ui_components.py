from pathlib import Path

import streamlit as st

from app.config import PORTFOLIO_ROOT
from app.health_overview import ProjectHealthStatus
from app.project_registry import PortfolioProject


def render_metric_card(
    label: str,
    value: str | int | float,
    help_text: str | None = None,
) -> None:
    """
    Render a Streamlit metric card.
    """
    st.metric(
        label=label,
        value=value,
        help=help_text,
    )


def render_project_card(project: PortfolioProject) -> None:
    """
    Render a single portfolio project card.
    """
    with st.container(border=True):
        st.subheader(project.name)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("Area")
            st.write(project.area)

        with col2:
            st.caption("Status")
            st.write(project.status)

        with col3:
            st.caption("Folder")
            st.code(project.folder_name, language="text")

        st.write(project.description)

        st.caption("Key features")

        for feature in project.key_features:
            st.write(f"- {feature}")

        with st.expander("Run commands"):
            st.write("Streamlit app:")
            st.code(project.streamlit_command, language="bash")

            st.write("Tests:")
            st.code(project.test_command, language="bash")

            st.write("Health check:")
            st.code(project.health_check_command, language="bash")


def render_projects_grid(projects: list[PortfolioProject]) -> None:
    """
    Render projects in a two-column grid.
    """
    for index in range(0, len(projects), 2):
        cols = st.columns(2)

        with cols[0]:
            render_project_card(projects[index])

        if index + 1 < len(projects):
            with cols[1]:
                render_project_card(projects[index + 1])


def render_capability_matrix(projects: list[PortfolioProject]) -> None:
    """
    Render a simple capability matrix for all projects.
    """
    rows = []

    for project in projects:
        features = ", ".join(project.key_features[:4])

        rows.append(
            {
                "Project": project.name,
                "Area": project.area,
                "Status": project.status,
                "Main capabilities": features,
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )


def render_health_table(statuses: list[ProjectHealthStatus]) -> None:
    """
    Render portfolio health overview as a table.
    """
    rows = []

    for status in statuses:
        rows.append(
            {
                "Project": status.project_name,
                "Status": status.status_label,
                "Checks": f"{status.passed_checks}/{status.total_checks}",
                "Screenshots": status.screenshot_count,
                "README": status.has_readme,
                "Streamlit": status.has_streamlit_app,
                "CLI": status.has_run_cli,
                "Tests": status.has_tests_dir,
                "Health Check": status.has_health_check,
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )


def render_project_screenshots(project: PortfolioProject) -> None:
    """
    Render screenshots for a project if they exist.
    """
    existing_screenshots = []

    for screenshot in project.screenshots:
        screenshot_path = PORTFOLIO_ROOT / screenshot

        if screenshot_path.exists() and screenshot_path.is_file():
            existing_screenshots.append(screenshot_path)

    if not existing_screenshots:
        st.info("No screenshots available for this project.")
        return

    for screenshot_path in existing_screenshots:
        st.image(
            str(screenshot_path),
            caption=screenshot_path.name,
            use_container_width=True,
        )


def render_architecture_overview() -> None:
    """
    Render a high-level architecture overview of the portfolio.
    """
    st.code(
        """
Generative AI Portfolio
│
├── RAG / Text
│   └── Document upload → Chunking → Embeddings → FAISS → LLM answer + sources
│
├── Vision
│   └── Image upload → Validation → Base64 encoding → Vision model → Answer + metadata
│
├── Voice / Audio
│   └── Audio upload → Transcription → Summarization → Structured result
│
└── MCP / Tools
    └── User command → Assistant router → Tools → Workspace manager → Safe file operations
        """,
        language="text",
    )


def render_engineering_practices() -> None:
    """
    Render shared engineering practices used across projects.
    """
    practices = [
        "Modular Python project structure",
        "Streamlit user interfaces",
        "Command-line entry points",
        "Environment-based configuration",
        ".env.example for safe setup",
        ".gitignore protection for secrets and generated files",
        "Structured logging",
        "Health check scripts",
        "Unit tests with pytest",
        "README documentation",
        "Demo screenshots",
        "Separation between UI, pipeline logic, and utility layers",
    ]

    for practice in practices:
        st.write(f"- {practice}")


def render_project_detail(project: PortfolioProject) -> None:
    """
    Render a detailed project section.
    """
    st.header(project.name)

    st.write(project.description)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Area", project.area)

    with col2:
        st.metric("Status", project.status)

    with col3:
        st.metric("Screenshots", len(project.screenshots))

    st.subheader("Key Features")
    for feature in project.key_features:
        st.write(f"- {feature}")

    st.subheader("Screenshots")
    render_project_screenshots(project)

    st.subheader("Run Locally")
    st.write("Streamlit:")
    st.code(project.streamlit_command, language="bash")

    st.write("Tests:")
    st.code(project.test_command, language="bash")

    st.write("Health Check:")
    st.code(project.health_check_command, language="bash")


def render_footer() -> None:
    """
    Render footer text.
    """
    st.divider()
    st.caption(
        "Multimodal AI Workspace — a unified overview of practical "
        "Generative AI projects across text, vision, audio, and tools."
    )