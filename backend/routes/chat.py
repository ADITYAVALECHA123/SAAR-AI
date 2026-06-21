from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.services.chat_services import ask_question_pipeline, ask_pdf_question_pipeline, ask_research_question, ask_video_question
from backend.security.auth_guard import get_current_user
from backend.services.chat_history_service import create_chat_session, save_chat_message, get_chat_messages, get_user_chat_sessions, get_chat_session
from backend.services.title_generator import generate_chat_title
from backend.models.chat_session import ChatSession
from backend.models.chat_message import ChatMessage
from backend.db.database import SessionLocal
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ChatRequest(BaseModel):
    message: str
    document_id: Optional[int]=None
    document_type: Optional[str]=None
    session_id: Optional[int]=None

@router.post("/")
async def chat(req: ChatRequest, current_user=Depends(get_current_user)):
    session_id = req.session_id
    if session_id:
        session = get_chat_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail = "Session not found")
        if session.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access Denied")
    else:
        title=generate_chat_title(req.message)
        session= create_chat_session(user_id = current_user.id, title=title)
        session_id= session.id
    chat_history = get_chat_messages(session_id)
    save_chat_message(session_id=session_id, role="user", content=req.message)
    if req.document_id and req.document_type == "pdf":
        answer, sources, retrieved_chunks = ask_pdf_question_pipeline(query=req.message,document_id=req.document_id, current_user_id=current_user.id, chat_history=chat_history)
    elif req.document_id and req.document_type == "video":
        answer, sources, retrieved_chunks = ask_video_question(query=req.message, document_id=req.document_id, current_user_id=current_user.id, chat_history=chat_history)
    elif req.document_id and req.document_type == "research":
        answer, sources, retrieved_chunks = ask_research_question(query=req.message, document_id=req.document_id, current_user_id=current_user.id, chat_history=chat_history)
    else:
        answer, sources, retrieved_chunks = ask_question_pipeline(query=req.message, current_user_id=current_user.id, chat_history=chat_history)
    save_chat_message(session_id=session_id, role="assistant", content=answer)

    return {
        "session_id":session_id,
        "response": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }

@router.get("/sessions")
async def get_sessions(current_user=Depends(get_current_user)):
    sessions = get_user_chat_sessions(current_user.id)
    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at,
            "updated_at": s.updated_at
        }
        for s in sessions
    ]

@router.get("/sessions/{session_id}")
async def load_session(session_id: int, current_user=Depends(get_current_user)):
    session = get_chat_session(session_id)
    if not session:
        raise HTTPException(status_code=404,detail="Session not found")
    if session.user_id!=current_user.id:
        raise HTTPException(status_code=403, detail="Access Denied")
    messages = get_chat_messages(session_id)
    return {
        "session_id": session_id,
        "messages": messages
    }

@router.delete("/session/{session_id}")
def delete_chat_session(session_id: int,current_user=Depends(get_current_user)):
    db = SessionLocal()
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).delete()

    db.delete(session)
    db.commit()

    return {
        "status": "success",
        "message": "Chat deleted"
    }