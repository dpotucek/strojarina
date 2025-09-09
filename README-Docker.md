# Strojarina Docker Setup

## Quick Start

### Using run script
```bash
./run-container.sh
```

### Using Docker directly
```bash
# Build image
docker build -t strojarina:latest .

# Run interactive container
docker run -it --rm -v "$(pwd)":/app -e PYTHONPATH=/app/src:/app strojarina:latest /bin/bash
```

### Using Docker Compose
```bash
# Interactive development
docker-compose run --rm strojarina

# Run tests
docker-compose run --rm strojarina-tests
```

## Inside Container

### Run modules
```bash
python src/deleni.py
python src/differentialThread.py
python src/knurling.py
```

### Run tests
```bash
poetry run pytest tests/testDeleni.py -v
```

### Python interactive
```bash
python3 -c "from deleni import DeliciHlava; h = DeliciHlava(); print(h.vypocti_pocet_der(40))"
```