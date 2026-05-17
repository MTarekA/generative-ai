from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

from app.config import get_settings, validate_openai_settings
from app.integrated_image_loader import (
    IntegratedImageLoader,
    IntegratedLoadedImage,
)


@dataclass
class IntegratedVisionResponse:
    """
    Structured response returned by the integrated vision pipeline.
    """

    answer: str
    question: str
    image_metadata: dict
    model: str


class IntegratedVisionPipeline:
    """
    Integrated vision-language pipeline for the Multimodal AI Workspace.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_openai_settings(self.settings)

        self.image_loader = IntegratedImageLoader()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def analyze_image(
        self,
        image_path: str | Path,
        question: str,
    ) -> IntegratedVisionResponse:
        """
        Analyze an image with a user question.
        """
        cleaned_question = question.strip()

        if not cleaned_question:
            raise ValueError("Question cannot be empty.")

        loaded_image = self.image_loader.load_image(image_path)

        answer = self._call_vision_model(
            loaded_image=loaded_image,
            question=cleaned_question,
        )

        return IntegratedVisionResponse(
            answer=answer,
            question=cleaned_question,
            image_metadata=self._extract_image_metadata(loaded_image),
            model=self.settings.openai_vision_model,
        )

    def _call_vision_model(
        self,
        loaded_image: IntegratedLoadedImage,
        question: str,
    ) -> str:
        """
        Call OpenAI vision-capable model.
        """
        response = self.client.chat.completions.create(
            model=self.settings.openai_vision_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful vision-language assistant. "
                        "Answer only based on what is visible in the image. "
                        "If something is unclear or not visible, say so clearly. "
                        "If the user asks in Arabic, answer in Arabic. "
                        "If the user asks in English, answer in English."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    f"data:{loaded_image.mime_type};base64,"
                                    f"{loaded_image.base64_data}"
                                )
                            },
                        },
                    ],
                },
            ],
        )

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("Vision model returned an empty response.")

        return answer

    def _extract_image_metadata(
        self,
        loaded_image: IntegratedLoadedImage,
    ) -> dict:
        """
        Extract clean image metadata.
        """
        return {
            "file_name": loaded_image.file_name,
            "file_extension": loaded_image.file_extension,
            "mime_type": loaded_image.mime_type,
            "width": loaded_image.width,
            "height": loaded_image.height,
            "mode": loaded_image.mode,
        }