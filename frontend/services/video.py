import requests
from frontend.config import BACKEND_URL

def upload_video(video_file,token):
    try:
        headers = {"Authorization":f"Bearer {token}"}
        files = {
            "file": (video_file.name, video_file,video_file.type)}
        response = requests.post(
            f"{BACKEND_URL}/videos/upload",
            headers=headers,
            files=files,
            timeout=600
        )
        if response.status_code == 200:
            return response.json()
        print(f"Video Upload Error: {response.status_code}")
        print(response.text)
        return None
    except Exception as e:
        print(f"Video Upload Exception: {e}")
        return None
    
def ask_video_question(
    question,
    token
):
    try:

        headers = {
            "Authorization":
            f"Bearer {token}"
        }

        response = requests.post(
            f"{BACKEND_URL}/videos/ask",
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
            f"Video QA Error: {e}"
        )

        return {
            "answer": "Backend Error",
            "sources": []
        }