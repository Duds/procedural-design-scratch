# Codebase Analysis

**Date:** 06/01/2025  
**Project:** Procedural Design - Organic 3D Structure Generation

## Executive Summary

This is a well-structured Python project for generating procedural 3D designs using reaction-diffusion and space colonisation algorithms. The codebase has been refactored into a professional, modular architecture with clear separation of concerns, comprehensive testing, and multiple interfaces (CLI, Jupyter, Streamlit).

## Architecture Overview

### Project Structure

```
procedural-design/
├── src/                    # Source code (main package)
│   ├── algorithms/         # Core generative algorithms
│   ├── geometry/           # 3D mesh operations
│   ├── pipelines/         # End-to-end workflows
│   ├── cli/               # Command-line tools
│   ├── app/               # Streamlit web application
│   ├── utils/             # Utility functions
│   └── visualization/     # Rendering utilities
├── tests/                  # Comprehensive test suite
├── notebooks/              # Jupyter notebooks for experimentation
├── docs/                   # Documentation
├── data/                   # Templates and parameters
└── outputs/                # Generated meshes and renders
```

### Key Components

#### 1. Algorithms (`src/algorithms/`)

**Gray-Scott Reaction-Diffusion** (`gray_scott.py`):
- **Purpose**: Simulates chemical reactions to produce organic patterns
- **Implementation**: Dual CPU (NumPy) and GPU (Taichi) backends
- **Features**:
  - Pattern presets: spots, stripes, waves, holes
  - Configurable feed/kill rates
  - GPU acceleration via Taichi (10-100x speedup)
  - Custom initial conditions support
- **Key Classes**:
  - `GrayScottConfig`: Configuration dataclass
  - `GrayScottSimulator`: Main simulator class

**Space Colonisation** (`space_colonization.py`):
- **Purpose**: Grows branch-like structures toward attractor points
- **Implementation**: NumPy-based iterative algorithm
- **Features**:
  - Configurable influence/kill radii
  - Step-based growth
  - Attractor-based guidance
- **Key Classes**:
  - `SpaceColonizationConfig`: Configuration dataclass
  - `SpaceColonizationAlgorithm`: Main algorithm class

**Tunnelling** (`tunnelling.py`):
- **Purpose**: Agent-based tunnelling through 3D scalar fields
- **Implementation**: Random walk agents that modify field values
- **Features**:
  - Random walk agent system
  - Configurable tunnel radius and reduction
  - Boundary-aware tunnelling

#### 2. Geometry (`src/geometry/`)

**Mesh Operations** (consolidated in `mesh_operations.py`):
- `primitives.py`: Basic 3D shapes (cylinders, profiles)
- `mesh_operations.py`: Comprehensive mesh operations (consolidated from mesh_ops.py):
  - Mesh validation and quality checks
  - Isosurface extraction from 3D fields
  - Mesh smoothing and remeshing
  - Displacement application
  - Mesh repair and analysis
  - Overhang analysis for 3D printing
- `boundaries.py`: Boundary and mask generation for 3D simulations:
  - Vase masks with tapering
  - Cylindrical and spherical masks
  - Box masks
- `tube_sweep.py`: Tube generation along paths
- `isosurface.py`: Isosurface extraction utilities

**Key Features**:
- Watertight mesh validation
- Comprehensive validation with detailed reporting
- Mesh repair and optimisation
- Boundary generation for 3D fields
- Mesh export (STL, OBJ, PLY, 3MF)

#### 3. Pipelines (`src/pipelines/`)

**Vase Pipeline** (`vase.py`):
- End-to-end vase generation workflow
- Combines Gray-Scott patterns with 3D geometry
- Supports multiple profile types (circle, square, hexagon)
- Configurable displacement and tapering

**Moss Pole Pipeline** (`moss_pole.py`):
- Generates perforated cylindrical structures
- Uses space colonisation for branch patterns
- Creates tunnels through walls
- Supports structural ribs

**Mesh Processor Pipeline** (`mesh_processor.py`):
- Applies patterns to existing template meshes
- Useful for post-processing CAD models

#### 4. CLI Tools (`src/cli/`)

- `generate_vase.py`: Command-line vase generation
- `generate_moss_pole.py`: Command-line moss pole generation
- `process_template.py`: Template mesh processing
- `commands.py`: Unified CLI interface

#### 5. Web Application (`src/app/`)

- `streamlit_app.py`: Interactive web interface
- Real-time parameter adjustment
- Live preview of generated meshes

## Technology Stack

### Core Dependencies
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing utilities
- **Taichi**: GPU acceleration (JIT compilation)
- **Trimesh**: 3D mesh operations
- **scikit-image**: Image processing and marching cubes

### Development Tools
- **Jupyter Lab**: Interactive development
- **Streamlit**: Web application framework
- **pytest**: Testing framework
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking

## Code Quality

### Strengths
1. **Modular Architecture**: Clear separation of concerns
2. **Type Hints**: Comprehensive type annotations
3. **Documentation**: Well-documented with docstrings
4. **Testing**: Comprehensive test suite
5. **Multiple Interfaces**: CLI, Jupyter, and web app
6. **GPU Support**: Taichi integration for performance
7. **Configuration**: Dataclass-based configs for all components

### Recent Improvements (2025)
1. ✅ **Module Consolidation**: Merged duplicate mesh_ops.py and mesh_operations.py
2. ✅ **Boundary Generation**: Added boundaries.py for 3D mask generation
3. ✅ **Tunnelling Algorithms**: Added tunnelling.py for agent-based field modification
4. ✅ **Notebook Utilities**: Standardised path setup with src/utils/notebook.py
5. ✅ **Notebook Template**: Created standard template for new experiments

### Areas for Improvement
1. **Error Handling**: Could benefit from more specific exception types
2. **Logging**: Consider adding structured logging
3. **Performance Profiling**: Add profiling utilities
4. **Documentation**: API documentation could be generated (Sphinx)
5. **3D RD Extension**: Full 3D Gray-Scott with spatial gradients (in progress)

## Key Algorithms

### Gray-Scott Reaction-Diffusion

**Mathematical Model**:
```
∂u/∂t = Du∇²u - uv² + F(1-u)
∂v/∂t = Dv∇²v + uv² - (F+k)v
```

**Parameters**:
- `F` (feed_rate): 0.01-0.08
- `k` (kill_rate): 0.045-0.065
- `Du`, `Dv`: Diffusion rates
- Resolution: 64-512 (typical: 256)
- Steps: 1000-20000

**Pattern Presets**:
- Spots: F=0.055, k=0.062
- Stripes: F=0.035, k=0.060
- Waves: F=0.014, k=0.054
- Holes: F=0.039, k=0.058

### Space Colonisation

**Algorithm**:
1. Place attractor points in space
2. For each attractor, find closest node within influence radius
3. Grow node toward attractor by step_size
4. Remove attractors within kill_radius of nodes
5. Repeat until convergence or max_iterations

**Parameters**:
- Attractor count: 500-5000
- Influence radius: 5-30 mm
- Kill radius: 1-10 mm
- Step size: 0.5-5 mm

## Usage Patterns

### 1. Jupyter Notebooks
- Primary interface for experimentation
- Located in `notebooks/`
- Example: `01_refactored_example.ipynb`

### 2. CLI Tools
- Batch processing
- Automation scripts
- Example: `python src/cli/generate_vase.py --pattern spots`

### 3. Python API
- Direct import and use
- Programmatic control
- Example: `from pipelines.vase import VasePipeline`

### 4. Streamlit App
- Interactive parameter exploration
- Real-time preview
- Example: `streamlit run src/app/streamlit_app.py`

## Testing

Test coverage includes:
- Algorithm correctness
- CPU/GPU consistency (Taichi)
- Mesh validation
- Pipeline integration
- Edge cases

Run tests: `pytest tests/ -v`

## Performance Considerations

1. **GPU Acceleration**: Use `use_gpu=True` for Taichi backend
2. **Resolution**: Lower resolution (64-128) for faster testing
3. **Steps**: Fewer steps (1000-5000) for quick iterations
4. **Memory**: Efficient field representations
5. **Batch Processing**: CLI tools support parallel execution

## Dependencies

See `requirements.txt` for complete list. Key dependencies:
- taichi>=1.7.0
- numpy>=1.21.0
- jupyterlab>=4.0.0
- trimesh>=3.9.0
- scikit-image>=0.19.0
- streamlit>=1.28.0

## Development Workflow

1. **Virtual Environment**: Use `venv/` (created)
2. **Jupyter**: Use `start_jupyter.sh` or `jupyter lab`
3. **Testing**: `pytest tests/ -v`
4. **Code Quality**: `black .`, `flake8 .`, `mypy .`

## File Organization

- **Source Code**: `src/` (package structure)
- **Tests**: `tests/` (mirrors `src/` structure)
- **Notebooks**: `notebooks/` (experiments and examples)
- **Documentation**: `docs/` (guides and API docs)
- **Data**: `data/` (templates, parameters)
- **Outputs**: `outputs/` (generated meshes, renders)

## Next Steps

1. **Explore Notebooks**: Start with `notebooks/01_refactored_example.ipynb`
2. **Run Tests**: Verify installation with `pytest tests/`
3. **Generate First Vase**: Use CLI or Python API
4. **Experiment**: Adjust parameters in Jupyter
5. **Read Documentation**: See `docs/QUICK_START.md` and `docs/REFACTORING_GUIDE.md`

## Notes

- Australian English spelling used throughout
- Type hints required for all functions
- Comprehensive docstrings in all modules
- Follows `.cursor/rules/` coding standards

