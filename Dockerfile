# Use Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies including Node.js LTS for Tailwind CSS
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    gettext \
    && curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies first (separate layer for better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy project code
COPY . .

# Install the project in editable mode
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Compile translation messages
RUN uv run python manage.py compilemessages

# Prepare static files with Tailwind CSS
RUN uv run python manage.py tailwind install
RUN uv run python manage.py tailwind build
RUN uv run python manage.py collectstatic --noinput

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run gunicorn
CMD ["uv", "run", "--no-sync", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "config.wsgi:application"]
