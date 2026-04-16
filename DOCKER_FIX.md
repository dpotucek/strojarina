# Docker Build Fix - Dependency Conflict Resolution

## Issue
Docker build was failing with dependency conflict:
```
ERROR: Cannot install daptools 1.1.0 and daptools 1.2.0 because these package versions have conflicting dependencies.
```

## Root Cause
Multiple versions of DaPTools wheels (1.1.0 and 1.2.0) could exist in:
- `wheels/` directory in strojarina
- `dist/` directory in DaPTools

This caused pip to fail during Docker build when trying to install all `.whl` files.

## Solution

### 1. Dockerfile
Modified to install only the latest version using version sort:
```dockerfile
RUN pip install $(ls /tmp/daptools-*.whl | sort -V | tail -1)
```
This ensures even if multiple wheels exist, only the highest version number is installed.

### 2. Makefile
Updated `update-daptools` and `build-deps` targets to copy only the latest wheel:
```makefile
rm -f wheels/daptools-*.whl
cp $$(ls -t ../DaPTools/dist/daptools-*.whl | sort -V | tail -1) wheels/
```

### 3. update-deps.sh
Added cleanup of old wheels before copying:
```bash
rm -f wheels/daptools-*.whl
```

## Prevention
- **Dockerfile**: Handles multiple wheel versions gracefully by selecting the latest
- **Makefile**: Copies only the latest version from DaPTools/dist
- **update-deps.sh**: Prevents accumulation of old versions
- **Docker cache**: Bypassed when needed with `--no-cache` flag

## Verification
```bash
# Test make commands
make build-deps          # Copies only latest wheel
make update-daptools     # Full update and rebuild

# Build container (works even with multiple wheels present)
docker build -t strojarina:latest .

# Test functionality
docker run --rm strojarina:latest python3 tests/testDeleni.py
docker run --rm strojarina:latest python3 tests/testTriangles.py

# Test web interface
make web
# or
docker run --rm -p 5000:5000 strojarina:latest python3 src/gui_deleni_web.py
```

## Results
✓ All tests pass successfully with DaPTools 1.2.0
✓ `make update-daptools` works correctly
✓ Only latest wheel version is used
✓ No dependency conflicts
