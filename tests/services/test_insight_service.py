from app.dependencies.database import SessionLocal
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.services.budget_service import BudgetService
from app.services.dashboard_service import DashboardService
from app.services.insight_service import InsightService

db = SessionLocal()

dashboard_service = DashboardService(
    DashboardRepository(db),
)

budget_service = BudgetService(
    BudgetRepository(db),
    CategoryRepository(db),
)

service = InsightService(
    dashboard_service,
    budget_service,
)


db.close()
