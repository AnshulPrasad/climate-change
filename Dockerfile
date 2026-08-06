# Base image
FROM python:3.13-slim

# System environment variables
ENV PYTHONUBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python depedencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

# Copy application source code
COPY . .

# Create target static files directory and create non-root user (UID 1000 required by Hugging Face)
RUN mkdir -p /app/staticfiles && \
    useradd -m -u 1000 user && \
    chown -R user:user /app

USER user

# Collect static files during build
RUN python django_app/manage.py collectstatic --noinput

# Expose port 7860
EXPOSE 7860

# Execute migrations and launch Gunicorn on 0.0.0.0:7860
CMD ["sh", "-c", "python django_app/manage.py migrate && gunicorn --bind 0.0.0.0:$PORT --chdir django_app config.wsgi:application"]