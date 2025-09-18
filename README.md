# Strojarina - Machining Tools & Calculations

Comprehensive toolset for machining calculations with modern web interface. Includes division head calculations, thread analysis, differential threading, and more.

## Features

### Web GUI Tools (Bilingual CZ/EN)
- **Dělicí hlava** - Division head and rotary table calculations
- **Diferenciální závit** - Differential threading calculations  
- **Dělicí kotouček** - Division plate disk calculations
- **Hledání závitů** - Thread database search (metric & imperial)
- **Rýhování** - Knurling calculations for textured surfaces
- **Plochy na hřídeli** - Shaft surface calculations
- **Ohýbání materiálu** - Material bending calculations
- **Řemenice** - Pulley calculations and ratios
- **Sinusová lišta** - Sine bar angle calculations
- **Závitníkové vrtáky** - Tapping drill size calculations
- **Trojúhelníky** - Right triangle and general triangle calculations with Mollweide verification

### Command Line Tools
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
- `triangles` - Right triangle calculations

## Quick Start

### Docker (Recommended)
```bash
# Build and start web interface
make web
# → Open http://localhost:5000

# Or build and run manually
make build
docker run --rm -d -p 5000:5000 strojarina:latest
```

### Available Commands
```bash
make build           # Build Docker image
make run             # Run interactive container
make test            # Run tests in container
make clean           # Clean Docker images
make update-daptools # Update dependencies and rebuild
make web             # Start web GUI on port 5000
```

## Dependencies
- **DaPTools** - Personal Python utility library (integrated as wheel)
- Python 3.9+
- Poetry for dependency management
- Flask for web interface

## Project Structure
```
strojarina/
├── src/                    # Application source code
│   ├── deleni.py          # Division head calculations
│   ├── differentialThread.py # Differential threading
│   ├── DivisionPlatePlain.py # Division plate calculations
│   ├── findThread.py      # Thread database search
│   ├── triangles.py       # Right triangle calculations
│   ├── gui_deleni_web.py  # Web GUI Flask server
│   └── templates/         # HTML templates for web GUI
├── tests/                 # Unit tests
│   ├── testDeleni.py      # Division head tests
│   ├── testTriangles.py   # Triangle calculation tests
│   └── ...                # Other test files
├── data/                  # Thread database files
├── wheels/                # DaPTools wheel distributions
├── Dockerfile             # Container definition
├── Makefile              # Automation commands
└── pyproject.toml        # Poetry configuration
```

## Web Interface Features

### Bilingual Support
- **Complete Czech/English localization** with language switcher
- **Consistent styling** across all tools with responsive design
- **Input validation** and user-friendly error messages
- **REST API endpoints** for all calculations

### Division Head Calculator
- **Ratio selection:** Dělicí hlava (40) or Stůl (120)
- **Dropdown selection** for hole counts (24-66)
- **Two main functions:**
  - **Dosažitelná dělení** - shows possible divisions for selected hole count
  - **Výpočet děr pro dělení** - calculates required holes for desired division

### Differential Threading
- Calculate thread combinations for custom pitches
- Support for both metric (mm) and imperial (TPI) threads
- Automatic validation of available thread pitches

### Division Plate Calculator
- Calculate small disk diameters for division without dividing head
- Input: number of divisions and main disk diameter
- Output: required small disk radius and diameter

### Thread Finder
- Search comprehensive thread database
- Filter by diameter or pitch
- Support for metric and imperial threads
- Tabular results with complete thread specifications

### Knurling Calculator
- Calculate knurling parameters for textured surfaces
- Input diameter and get optimal knurl count
- Professional knurling wheel specifications

### Shaft Surfaces Calculator
- Calculate square and hexagonal surfaces on shafts
- Input shaft diameter and get machining dimensions
- Depth and edge length calculations

### Material Bending Calculator
- Steel sheet bending calculations
- Input thickness, width, length and bending angle
- Calculate required force and bending parameters

### Pulley Calculator
- Two-pulley system calculations
- Calculate driven pulley diameter from ratios
- Belt length and speed ratio calculations

### Sine Bar Calculator
- Precision angle measurement tool calculations
- Input desired angle and sine bar length
- Calculate required gauge block height

### Tapping Drills Calculator
- Calculate drill diameter for threading
- Input thread diameter, pitch, and strength percentage
- Supports 60-85% thread engagement options

### Right Triangle Calculator
- Calculate missing parameters from various input combinations
- Support for: two sides, side+angle, hypotenuse+side, hypotenuse+angle
- Mollweide equation verification for mathematical accuracy
- Comprehensive input validation and error handling
- Area and perimeter calculations
- Height calculations to any side using formula: height = (2 × area) / base

### General Triangle Calculator
- Calculate any triangle from three parameters (sides/angles)
- Support for: three sides, two sides + angle, one side + two angles
- Law of sines and cosines implementation
- Triangle type detection (right, isosceles, equilateral)
- Mollweide equation verification for all triangle types
- Heron's formula for area calculation
- Height calculations to all three sides with validation

## Docker Usage

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

## Development

### Local Development
```bash
# Install dependencies
poetry install

# Run web server
poetry run python src/gui_deleni_web.py
```

### Inside Container
```bash
# Run modules
python src/deleni.py
python src/differentialThread.py
python src/knurling.py

# Run tests
poetry run pytest tests/testDeleni.py -v
python3 tests/testTriangles.py  # Right triangle tests

# Python interactive
python3 -c "from deleni import DeliciHlava; h = DeliciHlava(); print(h.vypocti_pocet_der(40))"
python3 -c "from triangles import RightTriangle; t = RightTriangle(a=3, b=4); print(t)"
python3 -c "from triangles import CommonTriangle; t = CommonTriangle(a=3, b=4, c=5); print(t)"
python3 -c "from triangles import RightTriangle; t = RightTriangle(a=3, b=4); print('Heights:', t.get_all_heights())"
```

### Docker Development
```bash
# Development with volume mount
docker run --rm -p 5000:5000 -v $(pwd):/app strojarina:latest
```

### Updating Dependencies
```bash
# Update DaPTools and rebuild
make update-daptools

# Or manually
./update-deps.sh
```