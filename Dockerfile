# ================================
# 1) Base image — slim Python 3.12
# ================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app


# ==================================
# 2) Install OS-level dependencies
# ==================================
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*


# ==================================
# 3) Install Python dependencies
# ==================================
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt


# ==================================
# 4) Copy application code
# ==================================
COPY . .

# Expose FastAPI port
EXPOSE 8000


# ==================================
# 5) Run server with Uvicorn (production)
# ==================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
