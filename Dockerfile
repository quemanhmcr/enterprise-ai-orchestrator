# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency resolution (optional but recommended in README)
RUN pip install uv

# Copy dependency files
COPY requirements.txt .
COPY pyproject.toml .

# Install dependencies
# We install into a virtual environment to easily copy it later
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies using pip (or uv pip install)
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim as runner

WORKDIR /app

# Create a non-root user
RUN groupadd -r crewai && useradd -r -g crewai crewai

# Install runtime dependencies (if any system libs are needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Set ownership to non-root user
RUN chown -R crewai:crewai /app

# Switch to non-root user
USER crewai

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Healthcheck (optional, if you have an API)
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint
ENTRYPOINT ["python", "main.py"]
CMD ["--orchestrate"]
