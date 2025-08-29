from api.v1.endpoints import auth, reports, users, stats, taxonomy, taxonomy_admin
from fastapi import APIRouter

# from backend.api.v1.endpoints import __taxonomy

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(taxonomy.taxonomy_router, prefix="/taxonomy", tags=["taxonomy"])
api_router.include_router(taxonomy_admin.taxonomy_admin, tags=["taxonomy-admin"])

