# strojarina
tools pro dílnu. 

Možná časem přehodit do angličtiny.

## Docker Usage

### Quick Start
```bash
# Build and run
make dev

# Or manually
./run-container.sh
```

### Available Commands
```bash
make build    # Build Docker image
make run      # Run interactive container
make test     # Run tests in container
make clean    # Clean Docker images
```

### Docker Compose
```bash
docker-compose run --rm strojarina        # Interactive
docker-compose run --rm strojarina-tests  # Run tests
```