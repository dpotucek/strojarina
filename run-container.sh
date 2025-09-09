#!/bin/bash

# Build and run strojarina container

echo "Building strojarina container..."
docker build -t strojarina:latest .

echo "Running strojarina container..."
docker run -it --rm \
  -v "$(pwd)":/app \
  -e PYTHONPATH=/app/src:/app \
  --name strojarina-dev \
  strojarina:latest /bin/bash