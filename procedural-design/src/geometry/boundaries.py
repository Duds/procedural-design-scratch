"""Boundary and shape generation utilities.

This module provides functions to generate masks and boundaries
for 3D reaction-diffusion simulations and mesh generation.
"""

from typing import Tuple
import numpy as np


def make_vase_mask(
    n: int = 64,
    radius_frac: float = 0.7,
    taper: float = 0.3
) -> Tuple[np.ndarray, np.ndarray]:
    """Create a vase-like mask in an n³ grid.
    
    Generates a boolean mask defining the interior of a tapered
    vase shape. The vase tapers from a wider base toward a narrower top.
    
    Args:
        n: Grid resolution (n×n×n)
        radius_frac: Base radius as fraction of half-grid (0-1)
        taper: Taper factor (0 = cylinder, higher = stronger taper toward top)
    
    Returns:
        Tuple of (mask, Z_norm) where:
        - mask: Boolean 3D array (True inside vase)
        - Z_norm: Normalised Z coordinates (0 bottom, 1 top)
        
    Example:
        >>> mask, z_norm = make_vase_mask(n=64, radius_frac=0.7, taper=0.3)
        >>> print(f"Vase volume: {mask.sum()} voxels")
    """
    lin = np.linspace(-1, 1, n)
    X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
    
    R_xy = np.sqrt(X**2 + Y**2)
    Z_norm = (Z + 1.0) / 2.0  # 0 bottom, 1 top
    
    base_radius = radius_frac
    radius_z = base_radius * (1.0 - taper * Z_norm)
    
    mask = R_xy <= radius_z
    return mask.astype(bool), Z_norm


def make_cylinder_mask(
    n: int = 64,
    radius_frac: float = 0.7
) -> Tuple[np.ndarray, np.ndarray]:
    """Create a cylindrical mask in an n³ grid.
    
    Args:
        n: Grid resolution (n×n×n)
        radius_frac: Radius as fraction of half-grid (0-1)
    
    Returns:
        Tuple of (mask, Z_norm) where:
        - mask: Boolean 3D array (True inside cylinder)
        - Z_norm: Normalised Z coordinates (0 bottom, 1 top)
    """
    return make_vase_mask(n=n, radius_frac=radius_frac, taper=0.0)


def make_sphere_mask(
    n: int = 64,
    radius_frac: float = 0.7
) -> np.ndarray:
    """Create a spherical mask in an n³ grid.
    
    Args:
        n: Grid resolution (n×n×n)
        radius_frac: Radius as fraction of half-grid (0-1)
    
    Returns:
        Boolean 3D array (True inside sphere)
    """
    lin = np.linspace(-1, 1, n)
    X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
    
    R = np.sqrt(X**2 + Y**2 + Z**2)
    mask = R <= radius_frac
    
    return mask.astype(bool)


def make_box_mask(
    n: int = 64,
    size_frac: float = 0.8
) -> np.ndarray:
    """Create a box/cube mask in an n³ grid.
    
    Args:
        n: Grid resolution (n×n×n)
        size_frac: Size as fraction of grid (0-1)
    
    Returns:
        Boolean 3D array (True inside box)
    """
    lin = np.linspace(-1, 1, n)
    X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
    
    half_size = size_frac
    mask = (
        (np.abs(X) <= half_size) &
        (np.abs(Y) <= half_size) &
        (np.abs(Z) <= half_size)
    )
    
    return mask.astype(bool)

