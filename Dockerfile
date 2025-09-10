FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install DaPTools from wheel
COPY wheels/*.whl /tmp/
RUN pip install /tmp/*.whl

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only=main

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/app/src:/app

# Default command
CMD ["python", "-c", "print('Strojarina tools ready. Available modules in src/: deleni, differentialThread, knurling, pulleys, etc.')"]