import requests
from frontend.config import BACKEND_URL

def generate_summary(filename, token):
    response = requests.post(
        f"{BACKEND_URL}/pdf/summary",
        params={"filename": filename},
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    return response.json()

def upload_pdf(file, token):
    files = {
        "file": (file.name, file, "application/pdf")
    }
    response = requests.post(
        f"{BACKEND_URL}/pdf/upload",
        files=files,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    return response.json()