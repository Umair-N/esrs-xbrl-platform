from api.v1.endpoints import auth, reports, users, stats, taxonomy_admin, taxonomy, context
from api.v1.endpoints.canvas import router as canvas_router
from api.v1.endpoints.report_pages import router as report_pages_router
from fastapi import APIRouter



api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(taxonomy.taxonomy_router, prefix="/taxonomy", tags=["taxonomy"])
api_router.include_router(taxonomy_admin.taxonomy_admin, tags=["taxonomy-admin"])
api_router.include_router(context.router, prefix="/contexts", tags=["context"])
api_router.include_router(report_pages_router, prefix="/reports")
# Mount routes for saving and retrieving canvas sessions. These endpoints
# live under ``/reports/canvas`` to avoid clashing with existing report
# routes (e.g., listing, upload). See schemas/canvas.py for request and
# response definitions.
api_router.include_router(canvas_router, prefix="/reports/canvas", tags=["canvas"])
