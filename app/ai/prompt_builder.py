class PromptBuilder:

    @staticmethod
    def build_insight_prompt(
        summary: dict,
        budgets: list,
        top_categories: list,
    ) -> str:

        prompt = f"""
You are a professional financial advisor.

Analyze the following financial data.

Summary:
- Total Income: {summary["total_income"]}
- Total Expense: {summary["total_expense"]}
- Current Balance: {summary["current_balance"]}

Budget Status:
"""

        for budget in budgets:
            prompt += (
                f"\n"
                f"- {budget.category}: "
                f"Budget={budget.budget}, "
                f"Spent={budget.spent}, "
                f"Remaining={budget.remaining}"
            )

        prompt += "\n\nTop Spending Categories:\n"

        for category in top_categories:
            prompt += (
                f"- {category.category}: "
                f"{category.amount}\n"
            )

        prompt += """

Provide:

1. Overall financial summary
2. Three important insights
3. Three recommendations

Return plain text only.
"""

        return prompt

    @staticmethod
    def build_chat_prompt(
        *,
        message: str,
        summary: dict,
        budgets: list,
        top_categories: list,
    ) -> str:

        prompt = f"""
You are FinPilot AI, an intelligent personal finance assistant.

Answer ONLY using the financial information below.

FINANCIAL SUMMARY

Total Income: ₹{summary["total_income"]}
Total Expense: ₹{summary["total_expense"]}
Current Balance: ₹{summary["current_balance"]}
Total Transactions: {summary["total_transactions"]}

BUDGET STATUS
"""

        for budget in budgets:
            prompt += (
                f"\n"
                f"- {budget.category}: "
                f"Budget ₹{budget.budget}, "
                f"Spent ₹{budget.spent}, "
                f"Remaining ₹{budget.remaining}"
            )

        prompt += "\n\nTOP SPENDING CATEGORIES\n"

        for category in top_categories:
            prompt += (
                f"- {category.category}: ₹{category.amount}\n"
            )

        prompt += f"""

USER QUESTION

{message}

Instructions:
- Answer clearly and professionally.
- Use only the information above.
- Do not make up financial data.
- If the information is insufficient, say so.
"""

        return prompt