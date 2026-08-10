from google import genai
from google.genai import errors

from app.core.settings import get_settings
from app.exceptions.ai import AIServiceException


class GeminiClient:
    def __init__(self):
        self.settings = get_settings()

        self.client = genai.Client(
            api_key=self.settings.GEMINI_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.settings.GEMINI_MODEL,
                contents=prompt,
            )

            return response.text

        except errors.APIError as exc:
            raise AIServiceException() from exc