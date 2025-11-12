FROM python:3.11-slim

# Core libs for typical generated code; include gurobipy (CPU only)
RUN pip install --no-cache-dir matplotlib gurobipy

# Create non-root user
RUN useradd -u 10001 -m executor
USER executor

# Sandbox workdir (code will be mounted read-only at /sandbox/code)
WORKDIR /sandbox