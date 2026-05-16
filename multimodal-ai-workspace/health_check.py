from app.config import (
    ASSETS_DIR,
    DATA_DIR,
    DIAGRAMS_DIR,
    LOGS_DIR,
    OUTPUTS_DIR,
    PROJECT_ROOT,
    SCREENSHOTS_DIR,
    ensure_directories,
)
from app.health_overview import (
    get_overall_portfolio_score,
    get_portfolio_health_overview,
)
from app.project_registry import get_projects


def check_pass(message: str) -> None:
    """
    Print a successful health check message.
    """
    print(f"[OK] {message}")


def check_warning(message: str) -> None:
    """
    Print a warning health check message.
    """
    print(f"[WARNING] {message}")


def check_fail(message: str) -> None:
    """
    Print a failed health check message.
    """
    print(f"[FAIL] {message}")


def check_project_structure() -> bool:
    """
    Check important files for the Multimodal AI Workspace.
    """
    required_files = [
        PROJECT_ROOT / "streamlit_app.py",
        PROJECT_ROOT / "health_check.py",
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / ".gitignore",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "pytest.ini",
        PROJECT_ROOT / "app" / "config.py",
        PROJECT_ROOT / "app" / "project_registry.py",
        PROJECT_ROOT / "app" / "health_overview.py",
        PROJECT_ROOT / "app" / "ui_components.py",
        PROJECT_ROOT / "app" / "logger.py",
        PROJECT_ROOT / "tests" / "test_project_registry.py",
        PROJECT_ROOT / "tests" / "test_health_overview.py",
    ]

    missing_files = [
        file_path
        for file_path in required_files
        if not file_path.exists()
    ]

    if not missing_files:
        check_pass("Project structure looks good.")
        return True

    check_fail("Some required files are missing:")
    for file_path in missing_files:
        print(f"      - {file_path}")

    return False


def check_directories() -> bool:
    """
    Check required directories.
    """
    ensure_directories()

    required_dirs = [
        ASSETS_DIR,
        SCREENSHOTS_DIR,
        DIAGRAMS_DIR,
        DATA_DIR,
        OUTPUTS_DIR,
        LOGS_DIR,
    ]

    missing_dirs = [
        directory
        for directory in required_dirs
        if not directory.exists()
    ]

    if not missing_dirs:
        check_pass("Required directories exist.")
        return True

    check_fail("Some required directories are missing:")
    for directory in missing_dirs:
        print(f"      - {directory}")

    return False


def check_registry() -> bool:
    """
    Check whether the project registry contains the expected projects.
    """
    projects = get_projects()

    if len(projects) != 4:
        check_fail(f"Expected 4 projects, found {len(projects)}.")
        return False

    missing_project_paths = [
        project
        for project in projects
        if not project.local_path.exists()
    ]

    if missing_project_paths:
        check_fail("Some registered projects do not exist:")
        for project in missing_project_paths:
            print(f"      - {project.name}: {project.local_path}")
        return False

    check_pass("Project registry contains 4 valid projects.")
    return True


def check_portfolio_health_overview() -> bool:
    """
    Check whether portfolio health overview can be generated.
    """
    try:
        statuses = get_portfolio_health_overview()
        score = get_overall_portfolio_score()

        if len(statuses) != 4:
            check_fail("Health overview does not contain 4 projects.")
            return False

        check_pass(
            "Portfolio health overview generated successfully. "
            f"Readiness score: {int(score['readiness_score'] * 100)}%"
        )

        for status in statuses:
            print(
                f"      - {status.project_name}: "
                f"{status.status_label} "
                f"({status.passed_checks}/{status.total_checks})"
            )

        return True

    except Exception as error:
        check_fail(f"Portfolio health overview failed: {error}")
        return False


def check_screenshots() -> bool:
    """
    Check whether registered projects have demo screenshots.
    """
    statuses = get_portfolio_health_overview()

    projects_without_screenshots = [
        status
        for status in statuses
        if status.screenshot_count == 0
    ]

    if not projects_without_screenshots:
        check_pass("All registered projects have screenshots.")
        return True

    check_warning("Some projects have no detected screenshots:")
    for status in projects_without_screenshots:
        print(f"      - {status.project_name}")

    return False


def run_health_check() -> None:
    """
    Run all health checks and print a summary.
    """
    print("=" * 80)
    print("Multimodal AI Workspace - Health Check")
    print("=" * 80)

    checks = {
        "project_structure": check_project_structure(),
        "directories": check_directories(),
        "registry": check_registry(),
        "portfolio_health": check_portfolio_health_overview(),
        "screenshots": check_screenshots(),
    }

    passed = sum(1 for result in checks.values() if result)
    total = len(checks)

    print("=" * 80)
    print("Summary")
    print(f"Passed checks: {passed}/{total}")

    if (
        checks["project_structure"]
        and checks["registry"]
        and checks["portfolio_health"]
    ):
        print("Core hub setup is valid.")
    else:
        print("Core hub setup needs attention.")

    if not checks["screenshots"]:
        print(
            "Screenshot warning does not necessarily break the dashboard, "
            "but it should be reviewed for portfolio quality."
        )


if __name__ == "__main__":
    run_health_check()