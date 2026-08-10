from unittest.mock import MagicMock, patch

from google.genai import errors

from app.ai.client import GeminiClient
from app.exceptions.ai import AIServiceException


def test_gemini_client_generate():
    mock_settings = MagicMock()
    mock_settings.GEMINI_API_KEY = "fake-api-key"
    mock_settings.GEMINI_MODEL = "fake-model"

    mock_genai_client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = "Hello! How can I help you?"

    mock_genai_client.models.generate_content.return_value = mock_response

    with patch(
        "app.ai.client.get_settings",
        return_value=mock_settings,
    ), patch(
        "app.ai.client.genai.Client",
        return_value=mock_genai_client,
    ):
        client = GeminiClient()

        result = client.generate("Say hello in one sentence.")

    assert result == "Hello! How can I help you?"

    mock_genai_client.models.generate_content.assert_called_once_with(
        model="fake-model",
        contents="Say hello in one sentence.",
    )


def test_gemini_client_handles_api_error():
    mock_settings = MagicMock()
    mock_settings.GEMINI_API_KEY = "fake-api-key"
    mock_settings.GEMINI_MODEL = "fake-model"

    mock_genai_client = MagicMock()

    api_error = errors.ServerError(
        503,
        {"error": {"message": "Gemini service unavailable"}},
    )

    mock_genai_client.models.generate_content.side_effect = api_error

    with patch(
        "app.ai.client.get_settings",
        return_value=mock_settings,
    ), patch(
        "app.ai.client.genai.Client",
        return_value=mock_genai_client,
    ):
        client = GeminiClient()

        try:
            client.generate("Say hello in one sentence.")
            raise AssertionError("Expected AIServiceException")
        except AIServiceException as exc:
            assert exc.status_code == 503
            assert exc.message == "AI service is temporarily unavailable."
            assert exc.__cause__ is api_error