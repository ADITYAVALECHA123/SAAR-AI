from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.security.auth_guard import get_current_user
from backend.services.pdf_service import process_pdf, summarize_pdf
from backend.models.document import Document
from sqlalchemy.orm import Session
from backend.dependency.dependencies import get_db
import os
import re
import hashlib

def clean_filename(filename):
    return re.sub(
        r'[\\/*?:"<>|]',
        "",
        filename
    )

def get_file_hash_from_bytes(content):
    return hashlib.sha256(
        content
    ).hexdigest()

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

MAX_FILE_SIZE = 50 * 1024 * 1024
UPLOAD_DIR = "data/pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    if not file.filename:
          raise HTTPException(status_code=400,detail="Invalid filename")
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF Files are Allowed! ")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400,detail="Invalid file type")
    contents= await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File Size Exceeds 50MB Limit")
    file_hash = get_file_hash_from_bytes(contents)
    existing = (db.query(Document).filter(Document.user_id == current_user.id, Document.file_hash == file_hash).first())
    if existing:
        raise HTTPException(status_code=400, detail="Document already uploaded")
    safe_filename = f"{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    doc = Document(filename=file.filename, filepath=file_path, user_id=current_user.id, source_type="pdf")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    try:
        result =process_pdf(file_path=file_path, user_id=current_user.id, document_id=doc.id, source_type="pdf" )
        doc.file_hash = file_hash
        doc.indexed_status = "indexed"
        db.commit()
        db.refresh(doc)
        return {
        "status": "success",
        "data": result}
    except Exception as e:
        doc.indexed_status="failed"
        db.commit()
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/summary")
async def generate_pdf_summary(filename: str, current_user=Depends(get_current_user)):
    file_path = os.path.join("data/pdfs",f"{current_user.id}_{filename}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="PDF not found")
    try:
        summary = summarize_pdf(file_path, llm="llama-3.3-70b-versatile")
        return {
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))