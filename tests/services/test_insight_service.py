from app.dependencies.database import SessionLocal
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository

from app.services.dashboard_service import DashboardService
from app.services.budget_service import BudgetService
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

print(service.generate_insights(user_id=1))

db.close()