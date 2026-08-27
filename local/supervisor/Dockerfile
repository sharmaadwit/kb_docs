FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY local/supervisor/requirements-supervisor.txt requirements-supervisor.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-supervisor.txt

# Copy project structure
COPY local/supervisor ./local/supervisor
COPY local/cache ./local/cache
COPY skill ./skill

# Create logs directory
RUN mkdir -p ./local/supervisor/logs

# Create non-root user for security
RUN groupadd -r supervisor && useradd -r -g supervisor supervisor
RUN chown -R supervisor:supervisor /app

# Switch to non-root user
USER supervisor

# Run supervisor agent on-demand
ENTRYPOINT ["python3", "-m", "local.supervisor.supervisor_agent"]
CMD ["--report"]
