import json
from pathlib import Path

from app.result_manager import ResultManager


def test_result_manager_saves_analysis_result(tmp_path: Path) -> None:
    """
    Test that ResultManager saves an analysis result as JSON.
    """
    manager = ResultManager(output_dir=tmp_path)

    output_path = manager.save_analysis_result(
        image_path="test_image.png",
        question="What is in this image?",
        answer="The image contains a simple test object.",
        image_metadata={
            "file_name": "test_image.png",
            "width": 100,
            "height": 50,
        },
    )

    assert output_path.exists()
    assert output_path.suffix == ".json"

    with open(output_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["question"] == "What is in this image?"
    assert data["answer"] == "The image contains a simple test object."
    assert data["image_metadata"]["file_name"] == "test_image.png"
    assert "result_id" in data
    assert "created_at" in data