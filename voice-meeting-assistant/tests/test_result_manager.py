import json
from pathlib import Path

from app.result_manager import ResultManager


def test_result_manager_saves_audio_analysis_result(tmp_path: Path) -> None:
    """
    Test that ResultManager saves an audio analysis result as JSON.
    """
    manager = ResultManager(output_dir=tmp_path)

    output_path = manager.save_audio_analysis_result(
        audio_path="test_audio.mp3",
        transcript="This is a test transcript.",
        summary="This is a test summary.",
        audio_metadata={
            "file_name": "test_audio.mp3",
            "file_extension": ".mp3",
            "file_size_bytes": 1000,
            "file_size_mb": 0.01,
        },
        transcription_model="gpt-4o-mini-transcribe",
        summary_model="gpt-4o-mini",
    )

    assert output_path.exists()
    assert output_path.suffix == ".json"

    with open(output_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["audio_path"] == "test_audio.mp3"
    assert data["transcript"] == "This is a test transcript."
    assert data["summary"] == "This is a test summary."
    assert data["audio_metadata"]["file_name"] == "test_audio.mp3"
    assert data["transcription_model"] == "gpt-4o-mini-transcribe"
    assert data["summary_model"] == "gpt-4o-mini"
    assert "result_id" in data
    assert "created_at" in data