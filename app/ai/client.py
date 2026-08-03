from google import genai

from app.core.settings import get_settings


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

        response = self.client.models.generate_content(
            model=self.settings.GEMINI_MODEL,
            contents=prompt,
        )

        return response.text