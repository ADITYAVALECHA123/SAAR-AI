from backend.utils.chunking import chunk_video
from backend.services.llm import generate_response
import re, os

def summarize_text(text, model="llama-3.3-70b-versatile"):
    chunks = chunk_video(text)
    if not chunks:
        return "No content to summarize"
    partial_summaries = []
    for chunk in chunks:
        prompt = f"Summarize this content clearly and concisely: \n{chunk}"
        res = generate_response(prompt, model=model)
        partial_summaries.append(str(res))
    combined = "\n".join(partial_summaries)
    final_prompt = f"""
Combine the following summaries into a final structured summary:
{combined}
"""
    final_res = generate_response(final_prompt, model=model)
    return str(final_res)

def clean_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

def save_summary(title, summary):
    title = clean_title(title)
    os.makedirs("data/summary", exist_ok=True)
    path = f"data/summary/{title}_summary.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(summary)
    print("✅ Summary saved:", path)
    return path

def extract_topics(text, model="llama-3.3-70b-versatile"):
    prompt = f"""
Extract the top 5 important topics from the following content.

Rules:
- Return only short topic names
- No numbering
- No explanation
- One topic per line
- Keep topics meaningful and specific

Content:
{text}
"""
    response = generate_response(prompt, model=model)
    raw = str(response)
    topics = [
        line.strip("-•1234567890. ").strip()
        for line in raw.split("\n")
        if line.strip()
    ]
    return topics[:10]

def generate_timeline_summary(text, model="llama-3.3-70b-versatile", duration_seconds=None):
    duration_text = "unknown duration"
    if duration_seconds:
        if duration_seconds < 60:
            duration_text = (f"{duration_seconds} seconds")
        else:
            minutes = round(duration_seconds / 60,1)
            duration_text = (f"{minutes} minutes")

    prompt = f"""
Create a timeline-based summary of this video.                                                          

Rules:
- Total video duration: {duration_text}
- Timeline must match actual duration
- Do NOT invent timestamps
- If video is short, use seconds
- If video is long, use minutes
- Create 4 to 6 timeline points
- Keep content short and meaningful
- Output ONLY timeline entries
- Only timeline point per line

Strict Format: 
0-10 sec → Introduction
10-25 sec → Main Topic
25-40 sec → Discussion
Content:
{text}
"""

    response = generate_response(prompt, model=model)
    return str(response)


def summarize_paper(title, abstract):

    prompt = f"""
Summarize this research paper abstract.
Rules:
- Explain the objective
- Explain the methodology
- Explain key findings
- Explain conclusion
- Keep it concise and structured
{abstract}
"""
    summary = generate_response(prompt,model="llama-3.3-70b-versatile")

    save_summary(title, summary)

    return summary