import os
import logging
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from rich.traceback import install
from rich.logging import RichHandler

from api.v1.api import api_router
from core.config import settings
from database.connection import db_manager

# Enable pretty tracebacks for easier debugging
install(show_locals=True)

# Ensure necessary directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

# Configure logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

console_handler = RichHandler(rich_tracebacks=True, markup=True)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)

# FastAPI lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    retries = 3
    for attempt in range(retries):
        if db_manager.is_connection_alive():
            logger.info("Database connection established")
            break
        else:
            logger.error(f"Database connection failed on attempt {attempt + 1}")
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
            else:
                raise Exception("Database connection failed after retries")

    yield

    # Cleanup connections at shutdown
    db_manager.close_all_connections()
    logger.info("Database connections closed")

# App instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="XBRL BACKEND",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Use the explicit list of allowed origins
    allow_credentials=True,  # Allow sending credentials (cookies, etc.)
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # Explicit allowed methods
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],  # Explicit allowed headers
)


@app.middleware("http")
async def auto_refresh_tokens(request: Request, call_next):
    response = await call_next(request)

    tokens = getattr(request.state, "new_tokens", None)
    if tokens:
        is_production = getattr(settings, "ENVIRONMENT", "development").lower() == "production"

        if is_production:
            same_site, secure_flag = "none", True   # HTTPS + cross-site
        else:
            same_site, secure_flag = "lax", False   # localhost HTTP (same-origin via proxy)

        try:
            response.set_cookie(
                key="access_token",
                value=tokens["access_token"],
                httponly=True,
                samesite=same_site,
                secure=secure_flag,
                max_age=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                path="/",
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh_token"],
                httponly=True,
                samesite=same_site,
                secure=secure_flag,
                max_age=int(settings.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60,
                path="/",
            )
        except KeyError:
            logger.warning("Tokens are incomplete or malformed in request.")

    return response

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIRECTORY), name="uploads")

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI Backend is running", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    db_healthy = db_manager.is_connection_alive()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": time.time(),  # Optional, provides last check time
        "version": settings.VERSION,
    }

# Global HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "A handled HTTP error occurred"},
    )

# Global unhandled exception handler
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )
