FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Initialize a minimal git repo to satisfy DVC (won't be used for version control)
RUN git config --global user.email "docker@container.local" && \
    git config --global user.name "Docker Container" && \
    git init && \
    git add -A 2>/dev/null || true && \
    git commit -m "Initial commit" --allow-empty 2>/dev/null || true

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ app/
COPY dvc.yaml dvc.yaml
COPY dvc.lock dvc.lock
COPY params.yaml params.yaml
COPY .dvc/ .dvc/
COPY src/ src/
# new door
# Create directories for DVC-managed outputs
RUN mkdir -p models data metrics plots

# Expose port
EXPOSE 8000

# When container starts: pull model and data from S3 via DVC, then launch API
# Use --no-scm to skip git checks during pull
CMD dvc config core.no_scm true && \
    dvc pull -v && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000

