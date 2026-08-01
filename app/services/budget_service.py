from decimal import Decimal

from app.exceptions.base import AppException
from app.models import Budget
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas import (
    BudgetCreate,
    BudgetResponse,
    BudgetStatusResponse,
    BudgetUpdate,
)


class BudgetNotFoundError(AppException):
    status_code = 404

    def __init__(self):
        super().__init__("Budget not found.")


class BudgetAccessDeniedError(AppException):
    status_code = 403

    def __init__(self):
        super().__init__(
            "You do not have permission to access this budget."
        )


class BudgetAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self):
        super().__init__(
            "Budget already exists for this category and month."
        )


class BudgetService:

    def __init__(
        self,
        repository: BudgetRepository,
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    def create_budget(
        self,
        data: BudgetCreate,
        user_id: int,
    ) -> BudgetResponse:

        category = self.category_repository.get_by_id(
            data.category_id
        )

        if category is None:
            raise AppException("Category not found.")

        if category.user_id != user_id:
            raise AppException(
                "You cannot use another user's category."
            )

        existing = self.repository.get_by_category_month(
            user_id=user_id,
            category_id=data.category_id,
            month=data.month,
            year=data.year,
        )

        if existing:
            raise BudgetAlreadyExistsError()

        budget = self.repository.create(
            amount=data.amount,
            month=data.month,
            year=data.year,
            category_id=data.category_id,
            user_id=user_id,
        )

        return BudgetResponse.model_validate(budget)

    def get_budgets(
        self,
        user_id: int,
    ) -> list[BudgetResponse]:

        budgets = self.repository.get_by_user(user_id)

        return [
            BudgetResponse.model_validate(budget)
            for budget in budgets
        ]

    def get_owned_budget(
        self,
        budget_id: int,
        user_id: int,
    ) -> Budget:

        budget = self.repository.get_by_id(budget_id)

        if budget is None:
            raise BudgetNotFoundError()

        if budget.user_id != user_id:
            raise BudgetAccessDeniedError()

        return budget

    def update_budget(
        self,
        budget: Budget,
        data: BudgetUpdate,
    ) -> BudgetResponse:

        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(budget, key, value)

        budget = self.repository.update(budget)

        return BudgetResponse.model_validate(
            budget
        )

    def delete_budget(
        self,
        budget: Budget,
    ) -> None:

        self.repository.delete(budget)

    def get_budget_status(
        self,
        user_id: int,
    ) -> list[BudgetStatusResponse]:

        rows = self.repository.get_budget_status(user_id)

        result = []

        for row in rows:
            budget = Decimal(row.budget)
            spent = Decimal(row.spent)

            remaining = budget - spent

            if budget > 0:
                percentage = float((spent / budget) * 100)
            else:
                percentage = 0.0

            if percentage < 80:
                status = "On Track"
            elif percentage <= 100:
                status = "Warning"
            else:
                status = "Exceeded"

            result.append(
                BudgetStatusResponse(
                    category=row.category,
                    budget=budget,
                    spent=spent,
                    remaining=remaining,
                    percentage_used=round(percentage, 2),
                    status=status,
                )
            )

        return result