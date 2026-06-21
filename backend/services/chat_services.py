from backend.services.embeddings import get_embedding
from backend.services.retriever import get_retriever
from backend.services.memory import build_chat_context
from backend.services.vector_store import load_pdf_vectorstore, load_video_vectorstore, load_research_vectorstore
from backend.services.reranker import rerank_documents, get_dynamic_top_k
from backend.services.query_expansion import expand_query
from backend.models.analytics import QueryLog
from backend.services.llm import generate_response
from backend.services.context_compressor import compress_context
from backend.db.database import SessionLocal
import time


def ask_question_pipeline(query, model="llama-3.3-70b-versatile", chat_history=None,  current_user_id=None, document_id=None):
    print("COMMON CHAT PIPELINE CALLED")
    if not query.strip():
        return ("Please enter a valid question.", [], [])
    embedding = get_embedding()
    pdf_db = load_pdf_vectorstore(embedding, current_user_id)
    video_db = load_video_vectorstore(embedding, current_user_id)
    research_db = load_research_vectorstore(embedding, current_user_id)
    if pdf_db is None and video_db is None and research_db is None:
        return ("❌ No documents uploaded yet.", [],[])
    chat_context = ""
    if chat_history:
        chat_context = build_chat_context(chat_history)
    enhanced_query = f"{chat_context}\nUser question: {query}"
    expanded_queries = expand_query(enhanced_query,model)[:3]
    docs = []
    if pdf_db:
        for q in expanded_queries:
            docs.extend(get_retriever(pdf_db, q, top_k=3, score_threshold=1.5))
    if video_db:
        for q in expanded_queries:
            docs.extend(get_retriever(video_db, q, top_k=3, score_threshold=1.5))
    if research_db:
        for q in expanded_queries:
            docs.extend(get_retriever(research_db, q, top_k=3, score_threshold=1.5))
    unique_docs = {}
    for doc in docs:
        key = doc.page_content.strip()
        unique_docs[key] = doc
    docs = list(unique_docs.values())
    if document_id is not None:
        docs = [d for d in docs if d.metadata.get("document_id")==document_id]
    print("=" * 50)
    print("QUERY:", query)
    print("EXPANDED QUERIES:", expanded_queries)
    print("TOTAL DOCS RETRIEVED:", len(docs))
    for i, d in enumerate(docs[:10]):
        print(f"DOC {i+1}")
        print("Metadata:", d.metadata)
        print("Content:", d.page_content[:200])
        print("-" * 30)
    print("=" * 50)
    if not docs:
        return ("❌ No relevant info found.", [], [])
    dynamic_top_k=min(get_dynamic_top_k(query), 5)
    docs = rerank_documents(query, docs, top_k=dynamic_top_k)
    print("AFTER RERANK:", len(docs))
    context = compress_context(docs)
    MAX_CONTEXT_CHARS = 15000
    context = context[:MAX_CONTEXT_CHARS]
    print("Context Length:", len(context))

    chat_context = ""
    if chat_history:
        chat_context = build_chat_context(chat_history)
    prompt = f"""
You are an expert research assistant.
Chat History:
{chat_context}
Use ONLY the provided context to answer the question.
Rules:
- If answer is found → explain clearly
- If partial → say "Based on available context..."
- If not found → say "Not in documents"
- Be structured and detailed
- Do NOT hallucinate
Context:
{context}
Question:
{query}
"""
    start = time.time()
    answer = generate_response(prompt, model=model, max_tokens=1050)
    end = time.time()
    source = "unknown"
    if docs:
        source = docs[0].metadata.get(
        "source_type",
        "unknown"
    )
    db = SessionLocal()
    try:
        log = QueryLog(query=query, response_time=(end - start) * 1000, source=source, user_id=current_user_id)
        db.add(log)
        db.commit()
    finally:
        db.close()
    sources = []
    for d in docs:
        source_type = d.metadata.get("source_type", "unknown")
        name = d.metadata.get("source_name") or d.metadata.get("title") or "unknown"
        sources.append(f"{source_type.upper()}: {name}")
    retrieved_chunks = []
    for d in docs:
        retrieved_chunks.append({
            "source_type": d.metadata.get("source_type","unknown"),
            "source_name": (d.metadata.get("source_name") or d.metadata.get( "title") or "unknown"),
            "page": d.metadata.get("page"),
            "score": round(d.metadata.get("retrieval_score",0.0),4),
            "preview": (d.page_content[:300] + "...")})
    return (answer, list(set(sources)), retrieved_chunks)

def ask_pdf_question_pipeline(query, document_id, model="llama-3.3-70b-versatile",chat_history=None, current_user_id=None):
    print("PDF PIPELINE CALLED")
    if not query.strip():
        return ("Please enter a valid question", [], [])
    embedding = get_embedding()
    pdf_db = load_pdf_vectorstore(embedding, current_user_id)
    if not pdf_db:
        return ("❌ No PDF documents found.", [], [])
    docs = get_retriever(pdf_db, query, top_k=15, score_threshold=1.5)
    print("=" * 50)
    print("Selected document_id:", document_id)
    for d in docs:
        print(d.metadata)
    print("=" * 50)
    docs=[d for d in docs if d.metadata.get("document_id")==document_id]
    if not docs:
        return ("❌ No relevant PDF content found.", [], [])
    docs = rerank_documents(query,docs,top_k=5)
    MAX_CONTEXT_CHARS = 15000
    context = "\n\n".join([d.page_content for d in docs])
    context = context[:MAX_CONTEXT_CHARS]
    chat_context = ""
    if chat_history:
        chat_context = build_chat_context(chat_history)
    prompt = f"""
You are a PDF document assistant.
Chat History:
{chat_context}
Use ONLY the provided PDF context.
Rules:
- Answer only from PDF content
- If not found → say "Not found in documents"
- Be structured and clear
- Do NOT hallucinate
Context:
{context}
Question:
{query}
"""
    answer = generate_response(prompt, model=model)
    sources = []
    for d in docs:
        source_type = d.metadata.get("source_type", "unknown")
        name = (d.metadata.get(
            "source_name") or d.metadata.get("title") or "unknown")
        page=d.metadata.get("page")
        if (source_type=="pdf" and page is not None):
            sources.append(f"PDF: {name} Page{page+1}")
        elif source_type == "video":
            sources.append(f"Video: {name}")
        elif source_type=="research":
            sources.append(f"Research: {name}")
        else:
            sources.append(f"{source_type.upper()}: {name}")
    retrieved_chunks = []
    for d in docs:
        retrieved_chunks.append({
            "source_type": d.metadata.get("source_type", "unknown"),
            "source_name": d.metadata.get("source_name", "unknown"),
            "page": d.metadata.get("page"),
            "preview": d.page_content[:300]})
    return (answer, list(set(sources)), retrieved_chunks)

def ask_video_question(query,document_id=None, model="llama-3.3-70b-versatile",chat_history=None, current_user_id=None):
    if not query.strip():
        return ("Please enter a valid question", [], [])
    embedding = get_embedding()
    video_db = load_video_vectorstore(embedding, current_user_id)
    if not video_db:
        return ("❌ No video data found.", [], [])
    docs = get_retriever(video_db, query, top_k=15, score_threshold=1.5)
    if document_id is not None:
        docs=[d for d in docs if d.metadata.get("document_id")==document_id]
    if not docs:
        return ("❌ No relevant video content found.", [],[])
    docs = rerank_documents(query,docs,top_k=5)
    context = compress_context(docs)
    chat_context = ""
    if chat_history:
        chat_context = build_chat_context(chat_history)
    prompt = f"""
You are an expert video analysis assistant.
Use ONLY the transcript context below.
Instructions:
- Answer comprehensively
- Combine information from multiple transcript chunks
- Use bullet points when useful
- Explain concepts clearly
- If information is not present in the transcript, respond exactly: "Not found in video."
- Do not hallucinate
- Do not use outside the knowledge

Chat History:
{chat_context}

Context:
{context}

Question:
{query}
"""
    answer = generate_response(prompt, model=model)
    sources = []
    for d in docs:
        title = d.metadata.get(
            "title",
            "Unknown Video"
        )
        sources.append(
            f"VIDEO: {title}"
        )
    retrieved_chunks = []

    for d in docs:
        retrieved_chunks.append({
            "source_type": d.metadata.get("source_type", "video"),
            "source_name": d.metadata.get("title", "Unknown Video"),
            "preview": d.page_content[:300]})
    return (answer, list(set(sources)), retrieved_chunks)

def ask_research_question(query,document_id=None,  model="llama-3.3-70b-versatile",chat_history=None, current_user_id=None):
    if not query.strip():
        return("Please enter a valid question", [], [])
    embedding = get_embedding()
    research_db = load_research_vectorstore(embedding, current_user_id)
    if not research_db:
        return ("❌ No research papers found.", [], [])
    docs = get_retriever(research_db, query)
    if document_id is not None:
        docs=[d for d in docs if d.metadata.get("document_id")==document_id]
    research_docs = []
    for d in docs:
        if d.metadata.get("source_type") == "research":
            research_docs.append(d)
    if not research_docs:
        return ("❌ No relevant research content found.", [], [])
    research_docs = rerank_documents(query,research_docs,top_k=5)
    context = compress_context(research_docs)
    chat_context = ""
    if chat_history:
        chat_context = build_chat_context(chat_history)
    prompt = f"""
You are a research paper assistant.
Chat History:
{chat_context}
Use ONLY the provided research paper context.
Rules:
- Answer only from research paper content
- If not found → say "Not found in research papers"
- Be clear, structured, and precise
- No hallucination
Context:
{context}
Question:
{query}
"""
    answer = generate_response(prompt, model=model)
    sources = []
    for d in research_docs:
        title = d.metadata.get("source_name","Unknown Paper")
        sources.append(f"RESEARCH: {title}")
    retrieved_chunks = []
    for d in research_docs:
        retrieved_chunks.append({
            "source_type": "research",
            "source_name": d.metadata.get("source_name", "Unknown Paper"),
            "preview": d.page_content[:300]})
    return (answer, list(set(sources)), retrieved_chunks)
  