from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.document import Document
from fastapi import HTTPException
import os
from backend.dependency.dependencies import get_db
from backend.security.auth_guard import get_current_user

router = APIRouter(prefix="/library",tags=["Library"])

@router.get("/documents")
def get_documents(
    current_user = Depends(get_current_user), 
    db:Session = Depends(get_db)
):
    docs = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "filepath": d.filepath,
            "source_type": d.source_type,
            "file_size": d.file_size,
            "page_count": d.page_count,
            "indexed_status": d.indexed_status,
            "created_at": d.created_at
        }
        for d in docs
    ]

@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document not found or access denied"
        )
    base_name = os.path.splitext(doc.filename)[0]
    if doc.filepath and os.path.exists(doc.filepath):
        os.remove(doc.filepath)
    summary_path = f"data/summary/{base_name}_summary.txt"
    if os.path.exists(summary_path):
        os.remove(summary_path)
    transcript_path = f"data/transcript/{base_name}.txt"
    if os.path.exists(transcript_path):
        os.remove(transcript_path)
    audio_path = f"data/audio/{base_name}.wav"
    if os.path.exists(audio_path):
        os.remove(audio_path)
    db.delete(doc)
    db.commit()
    return {
        "message": "Document deleted successfully"
    }