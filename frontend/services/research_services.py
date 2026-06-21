import requests
from frontend.config import BACKEND_URL

def search_papers(query, source="all", sort_by="relevance"):
    try:
        response = requests.get(
            f"{BACKEND_URL}/research/search_papers",
            params={
                "query": query,
                "source": source,
                "sort_by": sort_by
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Research Search Error: {e}")
        return []


def summarize_paper(title,summary):
    try:
        response = requests.post(
            f"{BACKEND_URL}/research/summarize",
            json={
                "title": title,
                "summary": summary
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("summary","")
        return "Failed to summarize paper."
    except Exception as e:
        print(f"Paper Summary Error: {e}")
        return "Failed to summarize paper."


def save_paper_library(title, authors, summary,pdf_url,token):
    try:
        headers = {
            "Authorization":f"Bearer {token}"
        }
        response = requests.post(
            f"{BACKEND_URL}/research/save",
            json={
                "title": title,
                "authors": authors,
                "summary": summary,
                "pdf_url": pdf_url
            },
            headers=headers,
            timeout=120
        )
        if response.status_code == 200:
            return response.json()
        return {"status": "failed"}
    except Exception as e:
        print(f"Save Paper Error: {e}")
        return {"status": "failed"}


def ask_research_question(
    question,
    token
):
    try:

        headers = {
            "Authorization":
            f"Bearer {token}"
        }

        response = requests.post(
            f"{BACKEND_URL}/research/ask",
            json={
                "question": question
            },
            headers=headers,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()

        return {
            "answer": "Backend Error",
            "sources": []
        }

    except Exception as e:

        print(
            f"Research QA Error: {e}"
        )

        return {
            "answer": "Backend Error",
            "sources": []
        }