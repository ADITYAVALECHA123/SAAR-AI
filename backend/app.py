from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import time
from backend.routes.test import router as test_router
from backend.routes.auth import router as auth_router
from backend.routes.dashboard import router as dashboard_router
from backend.routes.chat import router as chat_router
from backend.routes.analytics import router as analytics_router
from backend.routes.setting import router as setting_router
from backend.routes.videos import router as video_router
from backend.routes.library import router as library_router
from backend.routes.pdf import router as pdf_router
from backend.routes.research import router as research_router
from backend.core.logger import logger
import backend.db.init_db
logger.info("SAAR Backend Initializing")

app = FastAPI(title="SAAR AI System")

app.add_middleware(CORSMiddleware,allow_origins=["*"], allow_credentials=True,allow_methods=["*"], allow_headers=["*"],)

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {process_time}s"
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ---------------------------------------------------
# Startup Event
# ---------------------------------------------------

@app.on_event("startup")
async def startup_event():
    logger.info("SAAR Backend Started")

# ---------------------------------------------------
# Shutdown Event
# ---------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("SAAR Backend Stopped")

# ---------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")
    return JSONResponse(status_code=500,content={
            "status": "error",
            "message": "Internal Server Error"
        }
    )

app.include_router(test_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(setting_router)
app.include_router(video_router)
app.include_router(library_router)
app.include_router(pdf_router)
app.include_router(research_router)

@app.get("/")
async def home():
    return {"message": "SAAR Backend Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
