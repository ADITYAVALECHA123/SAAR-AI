from pydantic import BaseModel
from typing import Optional
class UserSettingsUpdate(BaseModel):
    selected_model: Optional[str] = None
    chunk_size: Optional[int] = None
    top_k: Optional[int] = None
    temperature: Optional[float] = None
    theme: Optional[str] = None
    font_size: Optional[str] = None