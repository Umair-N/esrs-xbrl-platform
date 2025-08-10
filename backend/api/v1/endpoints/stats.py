from fastapi import APIRouter, Depends
from models.user import User
from api.dep import require_admin
from api.dep import get_db
from services.stats_service import stats_service
router = APIRouter()

@router.get("/users", response_model=dict)
async def get_stats(admin_user: User = Depends(require_admin), db=Depends(get_db)):
    return stats_service.get_stats(db)