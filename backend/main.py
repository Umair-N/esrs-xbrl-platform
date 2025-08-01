import logging
import os
from contextlib import asynccontextmanager

from api.v1.api import api_router
from core.config import settings
from database.connection import db_manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

os.makedirs("logs", exist_ok=True)
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not db_manager.is_connection_alive():
        logging.error("Database connection failed on startup")
        raise Exception("Database connection failed")
    logging.info("Database connection established")

    yield

    # Shutdown
    db_manager.close_all_connections()
    logging.info("Database connections closed")


# App init
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI Backend with Authentication and File Management",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIRECTORY), name="uploads")

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI Backend is running", "version": "1.0.0"}


# Health check
@app.get("/health")
async def health_check():
    db_healthy = db_manager.is_connection_alive()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
    }
