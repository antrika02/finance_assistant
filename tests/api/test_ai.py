from unittest.mock import Mock

from app.dependencies.services import (
    get_chat_service,
    get_insight_service,
)
from app.main import app


def test_get_ai_insights(
    client,
    authenticated_headers,
):
    mock_service = Mock()

    mock_service.generate_insights.return_value = (
        "You are spending more on food this month."
    )

    app.dependency_overrides[
        get_insight_service
    ] = lambda: mock_service

    try:
        response = client.get(
            "/ai/insights",
            headers=authenticated_headers,
        )

        assert response.status_code == 200

        body = response.json()

        assert body["insights"] == (
            "You are spending more on food this month."
        )

        mock_service.generate_insights.assert_called_once()

        user_id = (
            mock_service.generate_insights.call_args.args[0]
        )

        assert isinstance(user_id, int)

    finally:
        app.dependency_overrides.pop(
            get_insight_service,
            None,
        )


def test_get_ai_insights_without_token(
    client,
):
    mock_service = Mock()

    app.dependency_overrides[
        get_insight_service
    ] = lambda: mock_service

    try:
        response = client.get(
            "/ai/insights",
        )

        assert response.status_code == 401

        mock_service.generate_insights.assert_not_called()

    finally:
        app.dependency_overrides.pop(
            get_insight_service,
            None,
        )


def test_chat_with_ai(
    client,
    authenticated_headers,
):
    mock_service = Mock()

    mock_service.chat.return_value = (
        "Your largest expense this month is rent."
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/ai/chat",
            json={
                "message": "What is my biggest expense?"
            },
            headers=authenticated_headers,
        )

        assert response.status_code == 200

        body = response.json()

        assert body["response"] == (
            "Your largest expense this month is rent."
        )

        mock_service.chat.assert_called_once()

        call_kwargs = (
            mock_service.chat.call_args.kwargs
        )

        assert isinstance(
            call_kwargs["user_id"],
            int,
        )

        assert (
            call_kwargs["message"]
            == "What is my biggest expense?"
        )

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )


def test_chat_with_ai_without_token(
    client,
):
    mock_service = Mock()

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/ai/chat",
            json={
                "message": "What is my biggest expense?"
            },
        )

        assert response.status_code == 401

        mock_service.chat.assert_not_called()

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )


def test_chat_with_ai_empty_message(
    client,
    authenticated_headers,
):
    mock_service = Mock()

    mock_service.chat.return_value = (
        "Please provide a question."
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/ai/chat",
            json={
                "message": ""
            },
            headers=authenticated_headers,
        )

        assert response.status_code == 200

        body = response.json()

        assert body["response"] == (
            "Please provide a question."
        )

        mock_service.chat.assert_called_once()

        call_kwargs = (
            mock_service.chat.call_args.kwargs
        )

        assert call_kwargs["message"] == ""

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )