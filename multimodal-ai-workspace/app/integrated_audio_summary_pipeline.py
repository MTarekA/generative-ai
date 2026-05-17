from dataclasses import dataclass

from openai import OpenAI

from app.config import get_settings, validate_openai_settings


@dataclass
class IntegratedAudioSummaryResponse:
    """
    Structured response returned by the integrated audio summary pipeline.
    """

    summary: str
    transcript: str
    model: str


class IntegratedAudioSummaryPipeline:
    """
    Integrated transcript summarization pipeline.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        validate_openai_settings(self.settings)

        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def summarize_transcript(
        self,
        transcript: str,
    ) -> IntegratedAudioSummaryResponse:
        """
        Summarize a transcript into structured meeting/study notes.
        """
        cleaned_transcript = transcript.strip()

        if not cleaned_transcript:
            raise ValueError("Transcript cannot be empty.")

        summary = self._call_summary_model(cleaned_transcript)

        if not summary.strip():
            raise ValueError("Summary model returned an empty response.")

        return IntegratedAudioSummaryResponse(
            summary=summary,
            transcript=cleaned_transcript,
            model=self.settings.openai_summary_model,
        )

    def _call_summary_model(
        self,
        transcript: str,
    ) -> str:
        """
        Call OpenAI chat model to summarize the transcript.
        """
        response = self.client.chat.completions.create(
            model=self.settings.openai_summary_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful audio summarization assistant. "
                        "Summarize only the provided transcript. "
                        "Do not invent action items, decisions, or facts. "
                        "If the transcript is in Arabic, answer in Arabic. "
                        "If the transcript is in English, answer in English. "
                        "Return a structured summary with: "
                        "1) Short summary, 2) Key points, 3) Action items, "
                        "4) Decisions, 5) Open questions, 6) Keywords."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Please summarize this transcript:\n\n"
                        f"{transcript}"
                    ),
                },
            ],
        )

        summary = response.choices[0].message.content

        if not summary:
            raise ValueError("OpenAI summary response did not contain content.")

        return summary