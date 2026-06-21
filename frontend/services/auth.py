import re
import requests
import streamlit as st
import os
BASE_URL = "http://localhost:8000"
BACKEND_URL = os.getenv("BACKEND_URL","http://127.0.0.1:8000")

# ─────────────────────────────────────────────
#  AUTH HELPERS
# ─────────────────────────────────────────────
def api_login(email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return res.json(), res.status_code
    except requests.exceptions.ConnectionError:
        return {"detail": "Backend server not running"}, 500
    except Exception as e:
        return {"detail": str(e)}, 500

def api_signup(name, email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/signup",
            json={
                "full_name": name,
                "email": email,
                "password": password
            }
        )
        return res.json(), res.status_code

    except requests.exceptions.ConnectionError:
        return {"detail": "Backend server not running"}, 500

    except Exception as e:
        return {"detail": str(e)}, 500

def validate_signup(name, email, password, confirm):
    if not name.strip():
        return "Name is required."
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Enter a valid email address."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if password != confirm:
        return "Passwords do not match."
    return None

def pw_strength(pw):
    score = 0
    if len(pw) >= 8:   score += 1
    if len(pw) >= 12:  score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pw): score += 1
    labels = ["", "Weak", "Fair", "Good", "Strong", "Very Strong"]
    colors = ["", "#F87171", "#FBBF24", "#60A5FA", "#34D399", "#10B981"]
    return score, labels[min(score, 5)], colors[min(score, 5)]