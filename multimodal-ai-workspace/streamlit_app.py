import streamlit as st

from app.config import ensure_directories, get_settings
from app.health_overview import (
    get_overall_portfolio_score,
    get_portfolio_health_overview,
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


def render_sidebar(project_names: list[str]) -> str:
    """
    Render sidebar navigation and return selected page.
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
        st.metric("Completed", len([p for p in projects if p.status == "Completed"]))

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
        project for project in projects if project.name == selected_project_name
    )

    render_project_detail(selected_project)


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

    render_footer()


if __name__ == "__main__":
    main()