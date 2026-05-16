from app.health_overview import (
    get_health_overview_as_dicts,
    get_overall_portfolio_score,
    get_portfolio_health_overview,
)


def test_health_overview_contains_four_projects() -> None:
    """
    Test that health overview includes all portfolio projects.
    """
    overview = get_portfolio_health_overview()

    assert len(overview) == 4


def test_health_status_has_valid_check_counts() -> None:
    """
    Test that each project health status has valid check counts.
    """
    overview = get_portfolio_health_overview()

    for status in overview:
        assert status.total_checks > 0
        assert 0 <= status.passed_checks <= status.total_checks


def test_overall_portfolio_score_is_valid() -> None:
    """
    Test that overall portfolio readiness score is between 0 and 1.
    """
    score = get_overall_portfolio_score()

    assert score["total_projects"] == 4
    assert 0 <= score["readiness_score"] <= 1


def test_health_overview_as_dicts() -> None:
    """
    Test health overview dictionary export.
    """
    overview_dicts = get_health_overview_as_dicts()

    assert len(overview_dicts) == 4
    assert "project_name" in overview_dicts[0]
    assert "status_label" in overview_dicts[0]