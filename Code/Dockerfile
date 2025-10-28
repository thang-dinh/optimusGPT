FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build dependencies for building wheels if necessary
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc git curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy project metadata first to leverage Docker layer caching
COPY pyproject.toml .
# If you have a lock file (poetry.lock or similar), copy it too for reproducible installs
# COPY poetry.lock .

# Copy the rest of the application
COPY . .

# Install Poetry (official installer) and use it to install dependencies
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION="2.2.1"
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
ENV PATH="$POETRY_HOME/bin:/root/.local/bin:$PATH"
# Configure Poetry to install into the system Python environment (do not create virtualenvs)
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

# Upgrade pip and let Poetry install dependencies from pyproject.toml
RUN poetry install --no-interaction --no-ansi --only main 

# Default command to run the application
CMD ["python", "main.py"]