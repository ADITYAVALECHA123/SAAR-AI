import requests
from frontend.config import BACKEND_URL

def get_analytics(token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(f"{BACKEND_URL}/analytics/",headers=headers,timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Analytics Error: {e}")
    return {}
