from decimal import Decimal


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