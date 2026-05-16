from dataclasses import dataclass, asdict
from pathlib import Path

from app.project_registry import PortfolioProject, get_projects


@dataclass(frozen=True)
class ProjectHealthStatus:
    """
    Health status for one portfolio project.
    """

    project_name: str
    folder_name: str
    exists: bool
    has_readme: bool
    has_streamlit_app: bool
    has_run_cli: bool
    has_health_check: bool
    has_tests_dir: bool
    has_requirements: bool
    has_env_example: bool
    screenshot_count: int
    passed_checks: int
    total_checks: int
    status_label: str


def check_project_health(project: PortfolioProject) -> ProjectHealthStatus:
    """
    Check whether a portfolio project has the expected structure.
    """
    project_path = project.local_path

    exists = project_path.exists()
    has_readme = (project_path / "README.md").exists()
    has_streamlit_app = (project_path / "streamlit_app.py").exists()
    has_run_cli = (project_path / "run.py").exists()
    has_health_check = (project_path / "health_check.py").exists()
    has_tests_dir = (project_path / "tests").exists()
    has_requirements = (project_path / "requirements.txt").exists()
    has_env_example = (project_path / ".env.example").exists()

    screenshot_count = count_existing_screenshots(project)

    checks = [
        exists,
        has_readme,
        has_streamlit_app,
        has_run_cli,
        has_health_check,
        has_tests_dir,
        has_requirements,
        has_env_example,
        screenshot_count > 0,
    ]

    passed_checks = sum(1 for check in checks if check)
    total_checks = len(checks)

    status_label = determine_status_label(
        passed_checks=passed_checks,
        total_checks=total_checks,
    )

    return ProjectHealthStatus(
        project_name=project.name,
        folder_name=project.folder_name,
        exists=exists,
        has_readme=has_readme,
        has_streamlit_app=has_streamlit_app,
        has_run_cli=has_run_cli,
        has_health_check=has_health_check,
        has_tests_dir=has_tests_dir,
        has_requirements=has_requirements,
        has_env_example=has_env_example,
        screenshot_count=screenshot_count,
        passed_checks=passed_checks,
        total_checks=total_checks,
        status_label=status_label,
    )


def count_existing_screenshots(project: PortfolioProject) -> int:
    """
    Count screenshots that exist on disk.
    """
    count = 0

    for screenshot in project.screenshots:
        screenshot_path = project.local_path.parent / screenshot

        if screenshot_path.exists() and screenshot_path.is_file():
            count += 1

    return count


def determine_status_label(
    passed_checks: int,
    total_checks: int,
) -> str:
    """
    Determine a readable health status label.
    """
    if passed_checks == total_checks:
        return "Excellent"

    if passed_checks >= total_checks - 1:
        return "Good"

    if passed_checks >= total_checks // 2:
        return "Needs Review"

    return "Incomplete"


def get_portfolio_health_overview() -> list[ProjectHealthStatus]:
    """
    Return health status for all registered projects.
    """
    return [
        check_project_health(project)
        for project in get_projects()
    ]


def get_health_overview_as_dicts() -> list[dict]:
    """
    Return health overview as dictionaries.
    """
    return [
        asdict(status)
        for status in get_portfolio_health_overview()
    ]


def get_overall_portfolio_score() -> dict:
    """
    Compute an overall portfolio readiness score.
    """
    statuses = get_portfolio_health_overview()

    total_passed = sum(status.passed_checks for status in statuses)
    total_possible = sum(status.total_checks for status in statuses)

    score = (
        round(total_passed / total_possible, 2)
        if total_possible
        else 0
    )

    return {
        "total_projects": len(statuses),
        "total_passed_checks": total_passed,
        "total_possible_checks": total_possible,
        "readiness_score": score,
    }


if __name__ == "__main__":
    overview = get_portfolio_health_overview()

    for status in overview:
        print("=" * 80)
        print(status.project_name)
        print("Status:", status.status_label)
        print("Checks:", f"{status.passed_checks}/{status.total_checks}")
        print("Screenshots:", status.screenshot_count)

    print("=" * 80)
    print("Overall:")
    print(get_overall_portfolio_score())