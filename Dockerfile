# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /code

# Install basic build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Install dependencies into /install using the PyTorch CPU index URL
RUN pip install --prefix=/install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# ==========================================
# Stage 2: Final Runtime Image
# ==========================================
FROM python:3.12-slim

WORKDIR /code

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONPATH=/code \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY src ./src

EXPOSE 8000

# Entry point
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]