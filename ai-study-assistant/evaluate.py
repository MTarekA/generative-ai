import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from app.config import PROJECT_ROOT
from app.rag_pipeline import RAGPipeline


REPORTS_DIR = PROJECT_ROOT / "reports"
EVALUATION_REPORT_PATH = REPORTS_DIR / "evaluation_report.json"


@dataclass
class EvaluationCase:
    """
    A single evaluation test case for the RAG pipeline.
    """

    question: str
    expected_keywords: list[str]
    should_have_sources: bool = True


EVALUATION_CASES = [
    EvaluationCase(
        question="What is Retrieval-Augmented Generation?",
        expected_keywords=["retrieval", "generation"],
    ),
    EvaluationCase(
        question="What are the main steps of a RAG pipeline?",
        expected_keywords=["document", "chunk", "embedding", "retrieval"],
    ),
    EvaluationCase(
        question="What is the capital city of Brazil?",
        expected_keywords=["could not find", "provided documents"],
        should_have_sources=False,
    ),
]


def normalize_text(text: str) -> str:
    """
    Normalize text for simple keyword matching.
    """
    return text.lower().strip()


def evaluate_case(
    pipeline: RAGPipeline,
    case: EvaluationCase,
) -> dict:
    """
    Evaluate a single test case.
    """
    response = pipeline.ask(case.question)
    answer = normalize_text(response.answer)

    keyword_results = {
        keyword: keyword.lower() in answer
        for keyword in case.expected_keywords
    }

    keywords_passed = all(keyword_results.values())

    if case.should_have_sources:
        sources_passed = len(response.sources) > 0
    else:
        sources_passed = True

    passed = keywords_passed and sources_passed

    return {
        "question": case.question,
        "expected_keywords": case.expected_keywords,
        "answer": response.answer,
        "keyword_results": keyword_results,
        "source_count": len(response.sources),
        "sources": response.sources,
        "should_have_sources": case.should_have_sources,
        "passed": passed,
    }


def save_evaluation_report(report: dict) -> None:
    """
    Save evaluation results as a JSON file.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(EVALUATION_REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


def run_evaluation() -> None:
    """
    Run all evaluation cases and save a structured report.
    """
    pipeline = RAGPipeline()
    results = []

    for case in EVALUATION_CASES:
        print("-" * 80)
        print(f"Question: {case.question}")

        try:
            result = evaluate_case(pipeline, case)
            results.append(result)

            print(f"Passed: {result['passed']}")
            print(f"Source count: {result['source_count']}")
            print(f"Keyword checks: {result['keyword_results']}")
            print("Answer preview:")
            print(result["answer"][:500])

        except Exception as error:
            result = {
                "question": case.question,
                "expected_keywords": case.expected_keywords,
                "passed": False,
                "error": str(error),
            }
            results.append(result)

            print("Passed: False")
            print(f"Error: {error}")

    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)

    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "total_cases": total_count,
        "passed_cases": passed_count,
        "failed_cases": total_count - passed_count,
        "pass_rate": round(passed_count / total_count, 2),
        "evaluation_cases": [asdict(case) for case in EVALUATION_CASES],
        "results": results,
    }

    save_evaluation_report(report)

    print("=" * 80)
    print("Evaluation Summary")
    print(f"Passed: {passed_count}/{total_count}")
    print(f"Pass rate: {report['pass_rate']}")
    print(f"Report saved to: {EVALUATION_REPORT_PATH}")

    if passed_count == total_count:
        print("All evaluation cases passed.")
    else:
        print("Some evaluation cases failed. Review the answers above.")


if __name__ == "__main__":
    run_evaluation()