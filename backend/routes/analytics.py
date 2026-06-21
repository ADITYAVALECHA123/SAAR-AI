from fastapi import APIRouter, Depends
from backend.security.auth_guard import get_current_user
from backend.services.analytics_services import get_analytics

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def analytics_dashboard(
    current_user=Depends(get_current_user)):
    print(get_analytics(current_user.id))
    analytics_data = get_analytics(current_user.id)
    return {
        "status": "success",
        "data": analytics_data
    }

