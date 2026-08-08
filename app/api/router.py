from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.routes.root import router as root_router
from app.api.v1.ai import router as ai_router
from app.api.v1.auth import router as auth_router
from app.api.v1.budgets import router as budget_router
from app.api.v1.categories import router as categories_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.export import router as export_router
from app.api.v1.pdf import router as pdf_router
from app.api.v1.reports import router as reports_router
from app.api.v1.transactions import router as transactions_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(transactions_router)
api_router.include_router(dashboard_router)
api_router.include_router(budget_router)
api_router.include_router(reports_router)
api_router.include_router(export_router)
api_router.include_router(pdf_router)
api_router.include_router(ai_router)
api_router.include_router(root_router)
