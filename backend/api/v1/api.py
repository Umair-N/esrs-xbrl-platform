from api.v1.endpoints import auth, reports, users, stats, taxonomy_admin, taxonomy, context, session
from fastapi import APIRouter



api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(taxonomy.taxonomy_router, prefix="/taxonomy", tags=["taxonomy"])
api_router.include_router(taxonomy_admin.taxonomy_admin, tags=["taxonomy-admin"])
api_router.include_router(context.router, prefix="/contexts", tags=["context"])
api_router.include_router(session.router, prefix="/sessions", tags=["sessions"])

