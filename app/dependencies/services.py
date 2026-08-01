from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.budget_repository import BudgetRepository

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.transaction_service import TransactionService
from app.services.dashboard_service import DashboardService
from app.services.budget_service import BudgetService
from app.repositories.report_repository import ReportRepository
from app.services.report_service import ReportService
from app.services.export_service import ExportService
from app.repositories.transaction_repository import TransactionRepository
from app.services.pdf_service import PDFService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    """
    Returns a UserService instance.
    """
    repository = UserRepository(db)
    return UserService(repository)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    """
    Returns an AuthService instance.
    """
    repository = UserRepository(db)
    return AuthService(repository)


def get_category_service(
    db: Session = Depends(get_db),
) -> CategoryService:
    """
    Returns a CategoryService instance.
    """
    repository = CategoryRepository(db)
    return CategoryService(repository)


def get_transaction_service(
    db: Session = Depends(get_db),
) -> TransactionService:
    """
    Returns a TransactionService instance.
    """
    return TransactionService(
        TransactionRepository(db),
        CategoryRepository(db),
    )


def get_dashboard_service(
    db: Session = Depends(get_db),
) -> DashboardService:
    """
    Returns a DashboardService instance.
    """
    return DashboardService(
        DashboardRepository(db),
    )


def get_budget_service(
    db: Session = Depends(get_db),
) -> BudgetService:
    """
    Returns a BudgetService instance.
    """
    return BudgetService(
        BudgetRepository(db),
        CategoryRepository(db),
    )

def get_report_service(
    db: Session = Depends(get_db),
) -> ReportService:
    return ReportService(
        ReportRepository(db),
    )

def get_export_service(
    db: Session = Depends(get_db),
) -> ExportService:

    return ExportService(
        TransactionRepository(db),
    )

def get_pdf_service(
    db: Session = Depends(get_db),
) -> PDFService:

    return PDFService(
        DashboardRepository(db),
        TransactionRepository(db),
    )