# Strojarina Docker Makefile

.PHONY: build run test clean

# Build Docker image
build:
	docker build -t strojarina:latest .

# Run interactive container
run:
	docker run -it --rm \
		-v "$(PWD)":/app \
		-e PYTHONPATH=/app/src:/app \
		--name strojarina-dev \
		strojarina:latest /bin/bash

# Run tests in container
test:
	docker run --rm \
		-v "$(PWD)":/app \
		-e PYTHONPATH=/app/src:/app \
		strojarina:latest \
		poetry run pytest tests/testDeleni.py tests/testDifferentialThread.py tests/testDivisionPlatePlain.py tests/testFindThread.py tests/testKnurling.py tests/testPlochyNaHrideli.py tests/testPulleys.py tests/testStrojarinaRuzna.py tests/testTappingDrills.py -v

# Clean Docker images
clean:
	docker rmi strojarina:latest || true

# Build and run
dev: build run