import requests

BASE_URL = "http://127.0.0.1:8000"

def fetch_documents(token):
    response = requests.get(
        f"{BASE_URL}/library/documents",
       headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return []
 

def delete_document(doc_id, token):
    response = requests.delete(
        f"{BASE_URL}/library/documents/{doc_id}",
        headers={"Authorization": f"Bearer {token}"})
    return response.json(), response.status_code