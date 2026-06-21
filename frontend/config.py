import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL","https://saar-ai-production.up.railway.app")

APP_NAME = "Saar"
APP_ICON = "📚"