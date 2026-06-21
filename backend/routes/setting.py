from fastapi import APIRouter, Depends
from backend.security.auth_guard import get_current_user
from backend.services.setting_service import save_user_settings, load_user_settings
from backend.schemas.setting_schema import UserSettingsUpdate


router = APIRouter(prefix="/settings",tags=["Settings"])

@router.get("/")
async def fetch_settings(
    current_user=Depends(get_current_user)
):
    settings = load_user_settings(current_user.id)
    return {
        "status": "success",
        "data": settings
    }

@router.put("/")
async def update_settings(
    payload: UserSettingsUpdate,
    current_user=Depends(get_current_user)
):
    result = save_user_settings(user_id=current_user.id,data=payload.model_dump(exclude_none=True))
    return {
        "status": "success",
        "data": result
    }