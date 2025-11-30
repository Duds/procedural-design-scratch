"""Notebook utilities for path setup and common imports.

This module provides utilities to standardise notebook setup,
particularly for adding the project root to sys.path so that
src/ modules can be imported reliably.
"""

import sys
from pathlib import Path
from typing import Optional


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """Find the procedural-design project root directory.
    
    Looks for the project root by searching for:
    - setup.py or pyproject.toml in procedural-design/
    - procedural-design/src/ directory
    
    Args:
        start_path: Path to start searching from (default: current working directory)
        
    Returns:
        Path to project root (procedural-design/)
        
    Raises:
        RuntimeError: If project root cannot be found
        
    Example:
        >>> root = find_project_root()
        >>> print(root)
        PosixPath('/path/to/procedural-design')
    """
    if start_path is None:
        start_path = Path.cwd()
    
    current = Path(start_path).resolve()
    
    # Look for procedural-design directory
    for parent in [current] + list(current.parents):
        # Check if this looks like procedural-design root
        if (parent / 'procedural-design' / 'setup.py').exists():
            return parent / 'procedural-design'
        if (parent / 'procedural-design' / 'src').exists():
            return parent / 'procedural-design'
        
        # Or if we're already in procedural-design
        if (parent / 'setup.py').exists() and (parent / 'src').exists():
            return parent
        if parent.name == 'procedural-design' and (parent / 'src').exists():
            return parent
    
    raise RuntimeError(
        f"Could not find procedural-design project root. "
        f"Searched from: {start_path}"
    )


def setup_notebook_paths(project_root: Optional[Path] = None) -> Path:
    """Add project root to sys.path for notebook imports.
    
    This function should be called at the beginning of notebooks
    to enable imports from src/ modules.
    
    Args:
        project_root: Explicit project root path (default: auto-detect)
        
    Returns:
        Path to project root
        
    Example:
        >>> # In a notebook cell:
        >>> from src.utils.notebook import setup_notebook_paths
        >>> root = setup_notebook_paths()
        >>> print(f"Project root: {root}")
        >>> # Now you can import from src/
        >>> from src.algorithms.gray_scott import GrayScottSimulator
    """
    if project_root is None:
        project_root = find_project_root()
    else:
        project_root = Path(project_root).resolve()
    
    project_root_str = str(project_root)
    
    # Add to sys.path if not already there
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    
    return project_root


def check_optional_import(module_name: str, package_name: Optional[str] = None) -> bool:
    """Check if an optional module can be imported.
    
    Args:
        module_name: Name of module to import
        package_name: Optional package name for pip install
        
    Returns:
        True if module can be imported, False otherwise
        
    Example:
        >>> if check_optional_import('taichi', 'taichi'):
        ...     print("Taichi available!")
        ... else:
        ...     print("Taichi not available - using CPU")
    """
    try:
        __import__(module_name)
        return True
    except ImportError:
        if package_name:
            print(f"⚠️  {package_name} not available. Install with: pip install {package_name}")
        return False


def get_notebook_environment_info() -> dict:
    """Get information about the notebook environment.
    
    Returns:
        Dictionary with environment information:
        - python_version: Python version string
        - notebook_type: 'jupyter' or 'colab' or 'unknown'
        - project_root: Path to project root (if found)
        - in_notebook: Whether running in a notebook
        
    Example:
        >>> info = get_notebook_environment_info()
        >>> print(f"Running in: {info['notebook_type']}")
    """
    info = {
        'python_version': sys.version,
        'notebook_type': 'unknown',
        'project_root': None,
        'in_notebook': False,
    }
    
    # Detect notebook environment
    try:
        get_ipython()  # type: ignore
        info['in_notebook'] = True
        
        # Try to detect Jupyter vs Colab
        try:
            import IPython
            if IPython.get_ipython() is not None:
                if 'google.colab' in str(IPython.get_ipython()):
                    info['notebook_type'] = 'colab'
                else:
                    info['notebook_type'] = 'jupyter'
        except Exception:
            info['notebook_type'] = 'jupyter'
    except NameError:
        info['in_notebook'] = False
        info['notebook_type'] = 'script'
    
    # Try to find project root
    try:
        info['project_root'] = str(find_project_root())
    except RuntimeError:
        pass
    
    return info


def print_notebook_setup_info():
    """Print helpful information about notebook setup.
    
    Call this in a notebook cell to display environment information
    and confirm imports are configured correctly.
    
    Example:
        >>> from src.utils.notebook import setup_notebook_paths, print_notebook_setup_info
        >>> setup_notebook_paths()
        >>> print_notebook_setup_info()
    """
    root = setup_notebook_paths()
    env = get_notebook_environment_info()
    
    print("=" * 60)
    print("📓 Notebook Setup Information")
    print("=" * 60)
    print(f"Project root: {root}")
    print(f"Environment: {env['notebook_type']}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"In notebook: {env['in_notebook']}")
    print()
    print("✅ Project root added to sys.path")
    print("✅ You can now import from src/ modules")
    print()
    print("Example imports:")
    print("  from src.algorithms.gray_scott import GrayScottSimulator")
    print("  from src.pipelines.vase import VasePipeline")
    print("=" * 60)
    
    # Check optional dependencies
    print("\n📦 Optional Dependencies:")
    optional_modules = [
        ('taichi', 'taichi'),
        ('igl', 'libigl or pyigl'),
        ('streamlit', 'streamlit'),
    ]
    
    for module, package in optional_modules:
        if check_optional_import(module, package):
            print(f"  ✅ {package} available")
        else:
            print(f"  ⚠️  {package} not available (optional)")

