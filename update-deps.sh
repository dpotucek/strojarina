#!/bin/bash
# Automatická aktualizace DaPTools závislosti

set -e  # Exit on error

echo "Updating DaPTools dependency..."

# Build DaPTools
echo "Building DaPTools wheel..."
cd ../DaPTools
poetry build

# Copy to strojarina
echo "Copying wheel to strojarina..."
cd ../strojarina
# Remove old wheels to avoid conflicts
rm -f wheels/daptools-*.whl
cp ../DaPTools/dist/*.whl wheels/

# Rebuild container
echo "Rebuilding Docker container..."
docker build -t strojarina:latest . --no-cache

echo "DaPTools updated successfully!"
echo "Run: docker run -it --rm strojarina:latest"