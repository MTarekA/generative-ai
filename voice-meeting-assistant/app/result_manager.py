import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.config import OUTPUTS_DIR, ensure_directories


class ResultManager:
    """
    Manage saving transcription and summary results to disk.
    """

    def __init__(self, output_dir: Path | None = None) -> None:
        ensure_directories()
        self.output_dir = output_dir or OUTPUTS_DIR

    def save_audio_analysis_result(
        self,
        audio_path: str | Path,
        transcript: str,
        summary: str,
        audio_metadata: dict,
        transcription_model: str,
        summary_model: str,
    ) -> Path:
        """
        Save a complete audio analysis result as a JSON file.

        Returns:
            Path to the saved JSON file.
        """
        timestamp = datetime.now().isoformat(timespec="seconds")
        result_id = uuid4().hex[:12]

        result = {
            "result_id": result_id,
            "created_at": timestamp,
            "audio_path": str(audio_path),
            "audio_metadata": audio_metadata,
            "transcription_model": transcription_model,
            "summary_model": summary_model,
            "transcript": transcript,
            "summary": summary,
        }

        file_name = f"audio_analysis_{result_id}.json"
        output_path = self.output_dir / file_name

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                result,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return output_path