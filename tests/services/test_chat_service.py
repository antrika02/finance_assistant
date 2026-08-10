from unittest.mock import MagicMock

from app.services.chat_service import ChatService


def test_chat():
    dashboard_service = MagicMock()
    budget_service = MagicMock()
    gemini_client = MagicMock()

    dashboard_service.get_summary.return_value = {
        "total_income": 50000,
        "total_expense": 20000,
        "current_balance": 30000,
        "total_transactions": 10,
    }

    budget_service.get_budget_status.return_value = []

    dashboard_service.get_top_spending_categories.return_value = []

    gemini_client.generate.return_value = (
        "You are spending within your current budget."
    )

    service = ChatService(
        dashboard_service=dashboard_service,
        budget_service=budget_service,
        client=gemini_client,
    )

    result = service.chat(
        user_id=1,
        message="How am I doing financially?",
    )

    assert result == "You are spending within your current budget."

    dashboard_service.get_summary.assert_called_once_with(1)

    budget_service.get_budget_status.assert_called_once_with(1)

    dashboard_service.get_top_spending_categories.assert_called_once_with(1)

    gemini_client.generate.assert_called_once()
