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

# Expose port for Render
EXPOSE 8000

# Install Gunicorn
RUN pip install --no-cache-dir gunicorn

# Collect static files if using S3 or local
# Uncomment if you configure STATIC_ROOT in settings.py
# RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "quequeue_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
