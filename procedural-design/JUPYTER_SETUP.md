# Jupyter Setup Complete ✅

## Installation Summary

Jupyter Lab has been successfully installed and configured for this project.

### What Was Installed

1. **Virtual Environment**: Created at `venv/`
2. **Jupyter Lab**: Version 4.5.0
3. **IPython Kernel**: Configured as "Python (Procedural Design)"
4. **All Dependencies**: Installed from `requirements.txt`

### How to Start Jupyter Lab

#### Option 1: Using the Startup Script (Recommended)
```bash
cd procedural-design
./start_jupyter.sh
```

#### Option 2: Manual Activation
```bash
cd procedural-design
source venv/bin/activate
jupyter lab
```

#### Option 3: Direct Command
```bash
cd procedural-design
venv/bin/jupyter lab
```

### Kernel Selection

When creating a new notebook, select the kernel:
- **"Python (Procedural Design)"** - This uses the project's virtual environment

### Project Structure in Jupyter

The notebooks are located in:
- `notebooks/01_refactored_example.ipynb` - Main example notebook
- `notebooks/experiments/` - Experimental notebooks
- `notebooks/archived_experiments/` - Archived experiments

### Importing Project Modules

**Recommended: Use Notebook Utilities**

In your notebooks, use the standardised notebook utilities for path setup:

```python
# Standard library
import sys
from pathlib import Path

# Set up notebook paths (automatically finds project root)
from src.utils.notebook import setup_notebook_paths, print_notebook_setup_info

project_root = setup_notebook_paths()
print_notebook_setup_info()

# Now you can import from src
from src.algorithms.gray_scott import GrayScottSimulator, GrayScottConfig
from src.pipelines.vase import VasePipeline, VaseConfig
```

**Alternative: Manual Path Setup**

If you prefer manual setup:

```python
import sys
from pathlib import Path

# Add project root to path
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now you can import from src
from src.algorithms.gray_scott import GrayScottSimulator, GrayScottConfig
from src.pipelines.vase import VasePipeline, VaseConfig
```

**Note**: See `notebooks/TEMPLATE.ipynb` for a complete example notebook template.

### Quick Test

Run this in a Jupyter cell to verify everything works:

```python
from src.utils.notebook import setup_notebook_paths, print_notebook_setup_info

# Set up paths
project_root = setup_notebook_paths()
print_notebook_setup_info()

# Test imports
from src.algorithms.gray_scott import GrayScottSimulator, GrayScottConfig

# Quick test
config = GrayScottConfig(pattern_type='spots')
sim = GrayScottSimulator(resolution=64, config=config)
sim.initialize_random(n_seeds=3, seed=42)
field = sim.run(steps=100)

print("✅ Jupyter setup working correctly!")
print(f"Field shape: {field.shape}")
```

### Troubleshooting

**Issue**: Kernel not found
- **Solution**: The kernel should be installed. If not, run:
  ```bash
  source venv/bin/activate
  python -m ipykernel install --user --name=procedural-design --display-name="Python (Procedural Design)"
  ```

**Issue**: Import errors
- **Solution**: Make sure you've added the project root to `sys.path` (see above)

**Issue**: Jupyter Lab doesn't start
- **Solution**: Make sure the virtual environment is activated and Jupyter Lab is installed:
  ```bash
  source venv/bin/activate
  pip install jupyterlab
  ```

### Next Steps

1. **Start Jupyter Lab**: Run `./start_jupyter.sh`
2. **Open Example Notebook**: Navigate to `notebooks/01_refactored_example.ipynb`
3. **Run All Cells**: Execute the example to see the pipeline in action
4. **Create New Notebook**: Start experimenting with your own parameters

### Additional Resources

- **Quick Start Guide**: `docs/QUICK_START.md`
- **Refactoring Guide**: `docs/REFACTORING_GUIDE.md`
- **Codebase Analysis**: `CODEBASE_ANALYSIS.md`
- **Main README**: `README.md`

