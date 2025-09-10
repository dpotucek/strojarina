# strojarina
Tools pro dílnu - machining calculations and utilities

Možná časem přehodit do angličtiny.

## Dependencies
- **DaPTools** - Personal Python utility library (integrated as wheel)
- Python 3.9+
- Poetry for dependency management

## Docker Usage

### Quick Start
```bash
# Build and run
make dev

# Update DaPTools dependency
make update-daptools

# Or manually
./run-container.sh
```

### Available Commands
```bash
make build           # Build Docker image
make run             # Run interactive container
make test            # Run tests in container
make clean           # Clean Docker images
make update-daptools # Update DaPTools and rebuild
make build-deps      # Only build DaPTools wheel
```

### Automated Dependency Updates
```bash
# Shell script method
./update-deps.sh

# Makefile method (recommended)
make update-daptools
```

### Docker Compose
```bash
docker-compose run --rm strojarina        # Interactive
docker-compose run --rm strojarina-tests  # Run tests
```

## Development Workflow

### When DaPTools changes:
1. **Automatic**: Git hook rebuilds wheel after commit
2. **Manual**: Run `make update-daptools` in strojarina
3. **Script**: Run `./update-deps.sh`

### Project Structure
```
strojarina/
├── src/           # Application source code
├── wheels/        # DaPTools wheel distributions
├── Dockerfile     # Container definition
├── Makefile       # Automation commands
└── update-deps.sh # Dependency update script
```

## Tools Available
- `deleni` - Division calculations
- `differential-thread` - Thread calculations
- `division-plate` - Division plate calculations
- `find-thread` - Thread finder
- `knurling` - Knurling calculations
- `material-ohyb` - Material bending
- `plochy-hridel` - Shaft surface calculations
- `pulleys` - Pulley calculations
- `sine-bar` - Sine bar calculations
- `strojarina-ruzna` - Various calculations
- `tapping-drills` - Tapping drill sizes