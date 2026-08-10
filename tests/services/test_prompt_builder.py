from types import SimpleNamespace

from app.ai.prompt_builder import PromptBuilder


def test_build_insight_prompt():
    summary = {
        "total_income": 50000,
        "total_expense": 20000,
        "current_balance": 30000,
    }

    budgets = [
        SimpleNamespace(
            category="Food",
            budget=10000,
            spent=7000,
            remaining=3000,
        )
    ]

    categories = [
        SimpleNamespace(
            category="Food",
            amount=7000,
        )
    ]

    prompt = PromptBuilder.build_insight_prompt(
        summary,
        budgets,
        categories,
    )

    assert "Total Income: 50000" in prompt
    assert "Total Expense: 20000" in prompt
    assert "Current Balance: 30000" in prompt

    assert "Food" in prompt
    assert "Budget=10000" in prompt
    assert "Spent=7000" in prompt
    assert "Remaining=3000" in prompt

    assert "Overall financial summary" in prompt
    assert "Three important insights" in prompt
    assert "Three recommendations" in prompt


def test_build_chat_prompt():
    summary = {
        "total_income": 50000,
        "total_expense": 20000,
        "current_balance": 30000,
        "total_transactions": 10,
    }

    budgets = [
        SimpleNamespace(
            category="Food",
            budget=10000,
            spent=7000,
            remaining=3000,
        )
    ]

    categories = [
        SimpleNamespace(
            category="Food",
            amount=7000,
        )
    ]

    prompt = PromptBuilder.build_chat_prompt(
        message="How am I doing financially?",
        summary=summary,
        budgets=budgets,
        top_categories=categories,
    )

    assert "Total Income: ₹50000" in prompt
    assert "Total Expense: ₹20000" in prompt
    assert "Current Balance: ₹30000" in prompt
    assert "Total Transactions: 10" in prompt

    assert "Food" in prompt
    assert "Budget ₹10000" in prompt
    assert "Spent ₹7000" in prompt
    assert "Remaining ₹3000" in prompt

    assert "How am I doing financially?" in prompt

    assert "Do not make up financial data." in prompt
    assert "If the information is insufficient, say so." in prompt
