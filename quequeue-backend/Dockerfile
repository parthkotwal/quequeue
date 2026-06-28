# ---------- Stage 1: Build dependencies ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Build dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: Final image ----------
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Gunicorn
RUN pip install --no-cache-dir gunicorn

# Railway sets $PORT dynamically
CMD gunicorn quequeue_project.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3
