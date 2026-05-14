import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.config import OUTPUTS_DIR, ensure_directories


class ResultManager:
    """
    Manage saving image analysis results to disk.
    """

    def __init__(self, output_dir: Path | None = None) -> None:
        ensure_directories()
        self.output_dir = output_dir or OUTPUTS_DIR

    def save_analysis_result(
        self,
        image_path: str | Path,
        question: str,
        answer: str,
        image_metadata: dict,
    ) -> Path:
        """
        Save a single image analysis result as a JSON file.

        Returns:
            Path to the saved JSON file.
        """
        timestamp = datetime.now().isoformat(timespec="seconds")
        result_id = uuid4().hex[:12]

        result = {
            "result_id": result_id,
            "created_at": timestamp,
            "image_path": str(image_path),
            "question": question,
            "answer": answer,
            "image_metadata": image_metadata,
        }

        file_name = f"analysis_{result_id}.json"
        output_path = self.output_dir / file_name

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                result,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return output_path