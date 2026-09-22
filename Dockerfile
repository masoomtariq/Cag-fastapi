# ==========================================
# Stage 1: Build stage
# ==========================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set working directory
WORKDIR /app

# Enable bytecode compilation and copy configuration files
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# ==========================================
# Stage 2: Final Runtime stage
# ==========================================
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system dependencies (Poppler) securely and clean up caches
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-installed virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Place the virtual environment at the beginning of the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy your actual source code
COPY src/ /app/src/

# Expose FastAPI's default port
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
