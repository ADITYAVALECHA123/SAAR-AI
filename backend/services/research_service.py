
import os
import re
import requests
import arxiv
from backend.db.database import SessionLocal
from backend.models.document import Document
from backend.services.pdf_service import get_file_hash
from backend.utils.pdf_parser import load_pdf
from backend.utils.chunking import chunk_docs
from backend.services.embeddings import get_embedding
from backend.services.vector_store import save_research_vectorstore

def search_arxiv(query, limit= 45):
    try:
        search = arxiv.Search(query=query, max_results=limit, sort_by=arxiv.SortCriterion.Relevance)
        client = arxiv.Client()
        results =[]
        for paper in client.results(search):
            results.append({
                "title": paper.title,
                "authors": ",".join([author.name for author in paper.authors]),
                "summary": paper.summary,
                "pdf_url": paper.pdf_url,
                "paper_url": paper.entry_id,
                "source": "arXiv",
                "year": paper.published.year,
                "published": paper.published.strftime("%Y-%m-%d")
            })
        return results
    except Exception as e:
        print("arXiv Error:", e)
        return []


def search_papers(query, source="all", sort_by="relevance"):
    papers = search_arxiv(query)
    if sort_by =="title":
        papers.sort(key=lambda x: x.get("title", "").lower())
    elif sort_by =="year":
        papers.sort(key=lambda x: x.get("year", 0), reverse=True)
    return papers

def save_paper_library(title,authors,summary,pdf_url, user_id):
    db = SessionLocal()
    try:
        existing = db.query(Document).filter(Document.user_id == user_id,Document.external_url == pdf_url).first()
        if existing:
            return "already exists"
        download_result = download_paper_pdf(title,pdf_url, user_id)
        status = download_result["status"]
        if status == "pdf unavailable":
            return "download failed"
        if status =="download failed":
            return "download failed"
        file_path = download_result["file_path"]
        file_hash= get_file_hash(file_path)
        
        
        doc = Document(
            filename=title,
            filepath=file_path,
            file_hash=file_hash,
            source_type="research",
            external_url=pdf_url,
            description=summary,
            authors=authors,
            indexed_status="processing",
            user_id=user_id
            )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        process_research_pdf(file_path=file_path, user_id=user_id, document_id=doc.id)
        doc.indexed_status = "indexed"
        db.commit()
        return "saved"
    except Exception as e:
        print("Save Paper Error:", e)
        return "Failed"
    finally:
        db.close()

def clean_title(title):
    return re.sub(r'[\\/*?:"<>|]',"",title)

def download_paper_pdf(title,pdf_url, user_id):
    os.makedirs("data/papers",exist_ok=True)
    safe_title = (f"{user_id}_"
                f"{clean_title(title)}")
    file_path = os.path.join("data/papers",f"{safe_title}.pdf")
    if os.path.exists(file_path):
        return file_path
    try:
        print("=" * 50)
        print("TITLE:", title)
        print("PDF URL:", pdf_url)
        response = requests.get(pdf_url, timeout=120, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        print("STATUS:", response.status_code)
        print("CONTENT TYPE:", response.headers.get("Content-Type"))
    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        return {
            "status": "download failed",
            "file_path": None
        }
    if response.status_code != 200:
        return {
            "status": "download failed",
            "file_path": None
        }
    content_type = response.headers.get("Content-Type","").lower()
    if "pdf" not in content_type:
        return {
            "status":"pdf unavailable",
            "file_path": None
        }
    
    with open(file_path, "wb") as f:
        f.write(response.content)
    return {
        "status": "success",
        "file_path": file_path
    }



def process_research_pdf(file_path, user_id, document_id):
    docs = load_pdf(file_path)
    filename = os.path.basename(file_path)
    file_hash = get_file_hash(file_path)
    for doc in docs:
        doc.metadata["document_id"] = document_id
        doc.metadata["source_type"] = "research"
        doc.metadata["source_name"] = filename
        doc.metadata["user_id"] = user_id
        doc.metadata["file_hash"] = file_hash
    chunks = chunk_docs(docs)
    embedding = get_embedding()
    save_research_vectorstore(chunks,embedding,user_id)
    return len(chunks)