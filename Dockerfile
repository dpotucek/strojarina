FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Install DaPTools from wheel (only latest version)
COPY wheels/*.whl /tmp/
RUN pip install $(ls /tmp/daptools-*.whl | sort -V | tail -1)

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install application and test dependencies (pytest is required by `make test`)
RUN poetry install --with dev

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/app/src:/app

# Expose port for web GUI
EXPOSE 5000

# Default command
CMD ["python", "src/flask_app.py"]