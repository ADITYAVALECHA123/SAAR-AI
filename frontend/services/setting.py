import requests
BASE_URL = "https://saar-ai-production.up.railway.app"
def fetch_settings(token):
    response = requests.get(
        f"{BASE_URL}/settings/",
        headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return None


def save_settings(token, payload):
    response = requests.put(
        f"{BASE_URL}/settings/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"})
    return response.json(), response.status_code