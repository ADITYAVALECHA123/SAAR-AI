from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.security.auth_guard import get_current_user
from backend.services.research_service import search_papers,save_paper_library
from backend.services.summarizer import summarize_paper
from backend.services.chat_services import ask_research_question
class SummaryRequest(BaseModel):
    title: str
    summary: str


class SavePaperRequest(BaseModel):
    title: str
    authors: str
    summary: str
    pdf_url: str


class ResearchQuestionRequest(BaseModel):
    question: str

router = APIRouter(prefix="/research", tags=["Research"])

@router.get("/search_papers")
def search(query: str, source:str="all", sort_by:str = "relevance"):
    if not query.strip():
        return []
    return search_papers(query=query, source=source, sort_by=sort_by)

@router.post("/summarize")
def summarize(req: SummaryRequest):
    return {"summary": summarize_paper(req.title, req.summary)}

@router.post("/save")
def save_paper(req: SavePaperRequest, current_user=Depends(get_current_user)):
    print("=" * 50)
    print("TITLE:", req.title)
    print("PDF_URL:", req.pdf_url)
    print("=" * 50)
    status = save_paper_library(req.title,req.authors,req.summary, req.pdf_url,current_user.id)
    return {"status": status}

@router.post("/ask")
def ask_research(req: ResearchQuestionRequest,current_user=Depends(get_current_user)):
    answer, sources, retrieved_chunks = (ask_research_question(query=req.question,current_user_id=current_user.id))
    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }
