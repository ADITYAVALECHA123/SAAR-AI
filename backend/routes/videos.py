from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.security.auth_guard import get_current_user
from backend.services.video_service import process_video
from backend.services.chat_services import ask_video_question
from pydantic import BaseModel
import os

class VideoQuestionRequest(BaseModel):
    question: str


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

UPLOAD_DIR = "data/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_video(file: UploadFile = File(...),current_user=Depends(get_current_user)):
    try:
        video_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
        contents = await file.read()
        with open(video_path, "wb") as f:
            f.write(contents)
        result = await process_video(video_path=video_path, title=file.filename, user_id=current_user.id)
        
        return {
        "status": "success",
        "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
def ask_video(
    req: VideoQuestionRequest,
    current_user=Depends(get_current_user)
):

    answer, sources, retrieved_chunks = ask_video_question(
        query=req.question,
        current_user_id=current_user.id
    )

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }