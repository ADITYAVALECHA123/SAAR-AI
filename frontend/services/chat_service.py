import requests
from frontend.config import BACKEND_URL

def send_chat(message, token=None, user_id=None, document_id=None, session_id=None):
    headers = {}
    if token:
        headers["Authorization"] = (f"Bearer {token}")

    response = requests.post(f"{BACKEND_URL}/chat/",
        json={
            "message": message,
            "user_id":user_id,
            "document_id":document_id,
            "session_id":session_id
        },
        headers=headers,
        timeout=120
    )
    if response.status_code!=200:
          return {
            "response": "Backend Error",
            "sources": [],
            "retrieved_chunks":[]
        }
    return response.json()

def fetch_chat_sessions(token=None):
    headers = {}
    if token:
        headers["Authorization"] = (f"Bearer {token}")
    response = requests.get(f"{BACKEND_URL}/chat/sessions",headers=headers,timeout=30)
    if response.status_code != 200:
        return []
    return response.json()

def load_chat_session(session_id,token=None):
    headers = {}
    if token:
        headers["Authorization"] = (f"Bearer {token}")
    response = requests.get(f"{BACKEND_URL}/chat/sessions/{session_id}",headers=headers,timeout=30)
    if response.status_code != 200:
        return {
            "messages": []
        }
    return response.json()
def delete_chat_session(session_id, token):
    response = requests.delete(
        f"{BACKEND_URL}/chat/session/{session_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response.json()