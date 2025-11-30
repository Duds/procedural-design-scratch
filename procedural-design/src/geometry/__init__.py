"""Geometry utilities for procedural mesh generation."""

from .primitives import (
    create_cylinder,
    create_sphere,
    create_torus,
    rounded_square_profile,
)
from .mesh_operations import (
    extract_isosurface,
    apply_displacement,
    smooth_mesh,
    validate_mesh,
)
from .tube_sweep import sweep_tube, create_profile
from .boundaries import (
    make_vase_mask,
    make_cylinder_mask,
    make_sphere_mask,
    make_box_mask,
)

__all__ = [
    'create_cylinder',
    'create_sphere',
    'create_torus',
    'rounded_square_profile',
    'extract_isosurface',
    'apply_displacement',
    'smooth_mesh',
    'validate_mesh',
    'sweep_tube',
    'create_profile',
    'make_vase_mask',
    'make_cylinder_mask',
    'make_sphere_mask',
    'make_box_mask',
]
