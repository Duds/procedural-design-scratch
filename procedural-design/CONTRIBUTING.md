# Contributing to Procedural Design

Thank you for your interest in contributing to the procedural design project! This guide will help you get started.

## Development Workflow

### 1. Setting Up Your Environment

```bash
# Clone the repository
git clone <repository-url>
cd procedural-design

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### 2. Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Verify installation
pytest tests/ -v
```

### 3. Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style (see below)
   - Add tests for new functionality
   - Update documentation

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

4. **Check code quality**
   ```bash
   black .          # Format code
   flake8 .         # Lint code
   mypy .           # Type checking
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: Description of changes"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Project Structure

```
procedural-design/
├── src/
│   ├── algorithms/      # Core generative algorithms
│   ├── geometry/        # Mesh operations and boundaries
│   ├── pipelines/       # End-to-end workflows
│   ├── cli/            # Command-line tools
│   ├── app/            # Streamlit web app
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── notebooks/          # Jupyter notebooks
│   ├── experiments/    # Experimental notebooks
│   └── TEMPLATE.ipynb  # Template for new experiments
├── docs/               # Documentation
└── outputs/            # Generated outputs
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints for all functions
- Use Australian English spelling
- Maximum line length: 100 characters

### Code Formatting

```bash
# Format code
black .

# Check formatting
black --check .
```

### Type Hints

Always use type hints:

```python
def process_mesh(
    mesh: trimesh.Trimesh,
    iterations: int = 3
) -> trimesh.Trimesh:
    """Process mesh with given iterations."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def generate_pattern(
    resolution: int = 256,
    steps: int = 10000
) -> np.ndarray:
    """Generate a reaction-diffusion pattern.
    
    Args:
        resolution: Grid resolution (square grid)
        steps: Number of simulation steps
        
    Returns:
        Pattern field as numpy array
        
    Raises:
        ValueError: If resolution is invalid
        
    Example:
        >>> field = generate_pattern(resolution=128, steps=5000)
        >>> plt.imshow(field)
    """
    ...
```

## Adding New Features

### Adding a New Algorithm

1. Create module in `src/algorithms/`
2. Define configuration dataclass
3. Implement algorithm class
4. Add to `src/algorithms/__init__.py`
5. Write tests in `tests/test_<algorithm>.py`
6. Update documentation

Example structure:

```python
# src/algorithms/my_algorithm.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class MyAlgorithmConfig:
    """Configuration for my algorithm."""
    param1: float = 1.0
    param2: int = 10

class MyAlgorithm:
    """My algorithm implementation."""
    def __init__(self, config: Optional[MyAlgorithmConfig] = None):
        self.config = config or MyAlgorithmConfig()
    
    def run(self) -> np.ndarray:
        """Run the algorithm."""
        ...
```

### Adding a New Pipeline

1. Create module in `src/pipelines/`
2. Define pipeline configuration
3. Implement pipeline class with `generate()` method
4. Add export and validation methods
5. Write tests
6. Create CLI command if needed

### Adding a New Notebook Experiment

1. Copy `notebooks/TEMPLATE.ipynb`
2. Update metadata and description
3. Use notebook utilities for path setup:
   ```python
   from src.utils.notebook import setup_notebook_paths
   project_root = setup_notebook_paths()
   ```
4. Import from `src/` modules (not standalone code)
5. Document parameters and results

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_gray_scott.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Place tests in `tests/` directory
- Mirror `src/` structure
- Use descriptive test names
- Test edge cases and errors

Example:

```python
# tests/test_my_algorithm.py
import pytest
from src.algorithms.my_algorithm import MyAlgorithm, MyAlgorithmConfig

def test_algorithm_basic():
    """Test basic algorithm functionality."""
    config = MyAlgorithmConfig(param1=1.0)
    algo = MyAlgorithm(config)
    result = algo.run()
    assert result.shape == (256, 256)

def test_algorithm_invalid_params():
    """Test algorithm with invalid parameters."""
    with pytest.raises(ValueError):
        config = MyAlgorithmConfig(param1=-1.0)
        algo = MyAlgorithm(config)
```

## Documentation

### Updating Documentation

- Update relevant `.md` files in `docs/`
- Keep docstrings current
- Update `CODEBASE_ANALYSIS.md` for major changes
- Update `GOALS.md` when completing milestones

### Adding Examples

- Add examples to `docs/examples/`
- Include code snippets
- Show expected outputs
- Reference in relevant documentation

## Commit Messages

Use semantic commit messages:

```
Add: New feature description
Fix: Bug description
Update: Changed feature description
Refactor: Refactoring description
Docs: Documentation change
Test: Test addition/change
```

## Pull Request Process

1. **Create pull request**
   - Clear title and description
   - Reference related issues
   - Include examples if applicable

2. **Code review**
   - Address review comments
   - Ensure all tests pass
   - Update documentation if needed

3. **Merge**
   - Squash commits if appropriate
   - Delete feature branch after merge

## Questions?

- Check `README.md` for overview
- See `docs/QUICK_START.md` for getting started
- Review `GOALS.md` for project direction
- Open an issue for questions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on collaboration

Thank you for contributing! 🎨

