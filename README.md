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
make web             # Start web GUI on port 5000
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
├── src/                    # Application source code
│   ├── deleni.py          # Division head calculations
│   ├── gui_deleni_web.py  # Web GUI Flask server

│   └── templates/         # HTML templates for web GUI
│       └── deleni.html    # Main web interface
├── wheels/                # DaPTools wheel distributions
├── Dockerfile             # Container definition
├── Makefile              # Automation commands
├── update-deps.sh        # Dependency update script

```

## GUI Interface

### Web GUI (Recommended)
```bash
# Start web interface
make web
# → Open http://localhost:5000 in browser

# Or manually
docker run --rm -d -p 5000:5000 strojarina:latest
```

### Features
- **Dělicí hlava calculator** with interactive web interface
- **Dropdown selection** for hole counts from predefined values
- **Integer-only inputs** for precise calculations
- **Two ratio parameters:** dividing head ratio and table ratio
- **Real-time calculations** via AJAX
- **Responsive design** works on all devices

## Tools Available
- `deleni` - Division calculations (with GUI)
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