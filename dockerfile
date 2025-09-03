FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# If your backend code lives in ./backend in the repo:
COPY backend/ /app/

# EXPOSE is optional for Cloud Run; if you keep it, align with default 8080
EXPOSE 8080

# Read Cloud Run's PORT env var (falls back to 8080 locally)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
