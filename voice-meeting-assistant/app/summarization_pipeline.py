from dataclasses import dataclass

from openai import OpenAI

from app.config import get_settings, validate_settings
from app.prompts import (
    MEETING_SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_PROMPT_TEMPLATE,
)


@dataclass
class SummaryResponse:
    """
    Structured response returned by the summarization pipeline.

    summary:
        Structured summary generated from the transcript.

    transcript:
        Original transcript used for summarization.

    model:
        Summarization model used.
    """

    summary: str
    transcript: str
    model: str


class SummarizationPipeline:
    """
    Transcript summarization pipeline.

    Responsibilities:
    - Accept a transcript
    - Send it to an LLM with a structured prompt
    - Return a structured meeting/audio summary
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_settings(self.settings)

        if self.settings.summarization_provider != "openai":
            raise ValueError(
                "This pipeline currently supports only "
                "SUMMARIZATION_PROVIDER=openai."
            )

        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def summarize_transcript(self, transcript: str) -> SummaryResponse:
        """
        Summarize a transcript using an LLM.
        """
        clean_transcript = transcript.strip()

        if not clean_transcript:
            raise ValueError("Transcript cannot be empty.")

        prompt = SUMMARY_USER_PROMPT_TEMPLATE.format(
            transcript=clean_transcript,
        )

        response = self.client.chat.completions.create(
            model=self.settings.openai_summary_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": MEETING_SUMMARY_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        summary = response.choices[0].message.content

        if not summary:
            raise ValueError("Summary model returned an empty response.")

        return SummaryResponse(
            summary=summary,
            transcript=clean_transcript,
            model=self.settings.openai_summary_model,
        )


if __name__ == "__main__":
    sample_transcript = """
    Generative AI is a type of artificial intelligence that can create new
    content. It can generate text, images, audio, code, and videos.
    In real projects, generative AI is often combined with tools, documents,
    and databases to make systems more useful and connected to real
    information.
    """

    pipeline = SummarizationPipeline()
    response = pipeline.summarize_transcript(sample_transcript)

    print("Summary:")
    print(response.summary)

    print("\nModel:")
    print(response.model)