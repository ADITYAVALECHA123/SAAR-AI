import requests
import streamlit as st
from frontend.config import BACKEND_URL

def fetch_dashboard():
    try:
        response = requests.get(
            f"{BACKEND_URL}/dashboard/stats",
            params={"user_id": st.session_state.user["id"]},
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=30
        )
        if response.status_code != 200:
            return {
                "success": False,
                "error": response.json().get(
                    "detail",
                    "Failed to fetch dashboard"
                )
            }
        return {
            "success": True,
            "data": response.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Backend server offline"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }