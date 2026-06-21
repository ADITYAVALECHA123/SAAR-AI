import os
from backend.services.audio_service import extract_upload_audio, split_audio
from backend.services.transcription_service import transcribe_audio
from backend.services.summarizer import summarize_text, save_summary, extract_topics, clean_title, generate_timeline_summary
from backend.utils.chunking import chunk_video
from backend.services.embeddings import get_embedding
from backend.services.vector_store import save_video_vectorstore
from backend.db.database import SessionLocal
from backend.models.document import Document






def get_transcript(url, audio_path):    
    try:
        text= transcribe_audio(audio_path)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    return text

def save_transcript(title, text, user_id):
    title = (
    f"{user_id}_"
    f"{clean_title(title)}")
    os.makedirs("data/transcript", exist_ok=True)
    path = f"data/transcript/{title}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Transcript saved:", path)
    return path

async def process_video(video_path,title,user_id,model="llama-3.3-70b-versatile",chunk_size=1024):
    print("Extracting audio...")
    audio_path = extract_upload_audio(video_path,title,user_id=user_id)
    print("Transcribing...")
    try:
        audio_chunks = split_audio(audio_path)
        transcript_parts = []
        for chunk in audio_chunks:
            text = transcribe_audio(chunk)
            if text and text.strip():
                transcript_parts.append(text)
            if os.path.exists(chunk):
                os.remove(chunk)
        transcript = "\n".join(transcript_parts)
        if not transcript or not transcript.strip():
            return None
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    transcript_path = save_transcript(title,transcript,user_id)
    print("Summarizing...")
    summary = summarize_text(transcript,model=model)
    save_summary(title,summary)
    topics = extract_topics(summary,model=model)
    timeline_summary = (generate_timeline_summary(transcript,model=model))
    print("Embedding...")
    chunks = chunk_video(transcript,chunk_size=chunk_size,chunk_overlap=int(chunk_size * 0.2))
    for chunk in chunks:
        chunk.metadata["title"] = title
        chunk.metadata["source"] = title
        chunk.metadata["source_type"] = "video"
        chunk.metadata["user_id"] = user_id

    embedding = get_embedding()
    save_video_vectorstore(chunks,embedding,user_id)
    db = SessionLocal()
    try:
        existing = (db.query(Document).filter(Document.filename == title,Document.user_id == user_id).first())
        if not existing:
            doc = Document(filename=title,filepath=transcript_path,source_type="video",user_id=user_id,indexed_status="indexed")
            db.add(doc)
            db.commit()
    finally:
        db.close()
    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "topics": topics,
        "timeline_summary": timeline_summary
    }