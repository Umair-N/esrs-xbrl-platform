
# File: config.py
import os
from passlib.context import CryptContext

# Database configuration
DATABASE_URL = "auth.db"

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# File upload configuration
UPLOAD_DIRECTORY = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

ALLOWED_ORIGINS = ["http://localhost:3000" , "https://esrs-xbrl-platform.vercel.app/ " , "https://esrs-xbrl-platform.vercel.app"]

