FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION="2.2.1" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# System deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc git curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
ENV PATH="$POETRY_HOME/bin:/root/.local/bin:$PATH"

# Copy dependency files first for caching
COPY pyproject.toml .
# COPY poetry.lock .  # uncomment if present

# Install Python deps from pyproject (no groups → installs [project.dependencies])
RUN poetry install --no-ansi

# Copy the rest of the app
COPY . .

# Default command
CMD ["python", "main.py"]