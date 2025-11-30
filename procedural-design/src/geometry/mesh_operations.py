"""Mesh operations for procedural generation.

This module provides comprehensive mesh operations including:
- Isosurface extraction from 3D fields
- Mesh validation for 3D printing
- Smoothing and remeshing operations
- Displacement and pattern application
- Mesh repair and analysis utilities
"""

from typing import Optional, Tuple, Dict, Any
import numpy as np
import trimesh
from skimage import measure


def extract_isosurface(
    field: np.ndarray,
    isovalue: float = 0.5,
    spacing: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    smooth: bool = True,
    smooth_iterations: int = 3
) -> trimesh.Trimesh:
    """Extract isosurface from 3D scalar field using marching cubes.
    
    Args:
        field: 3D scalar field
        isovalue: Isosurface threshold value
        spacing: Voxel spacing in (x, y, z)
        smooth: Apply Laplacian smoothing
        smooth_iterations: Number of smoothing iterations
        
    Returns:
        Extracted mesh
        
    Raises:
        ValueError: If field is not 3D
        
    Example:
        >>> field = np.random.rand(100, 100, 100)
        >>> mesh = extract_isosurface(field, isovalue=0.5)
        >>> mesh.export('surface.stl')
    """
    if field.ndim != 3:
        raise ValueError(f"Field must be 3D, got shape {field.shape}")
    
    # Extract surface using marching cubes
    vertices, faces, normals, values = measure.marching_cubes(
        field,
        level=isovalue,
        spacing=spacing
    )
    
    # Create mesh
    mesh = trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
        vertex_normals=normals,
        process=True
    )
    
    # Optional smoothing
    if smooth:
        mesh = smooth_mesh(mesh, iterations=smooth_iterations)
    
    return mesh


def apply_displacement(
    mesh: trimesh.Trimesh,
    displacement_field: np.ndarray,
    amplitude: float = 1.0,
    along_normal: bool = True
) -> trimesh.Trimesh:
    """Apply displacement to mesh vertices.
    
    Args:
        mesh: Input mesh
        displacement_field: Displacement values (one per vertex or interpolated)
        amplitude: Displacement amplitude scaling
        along_normal: Displace along vertex normals (vs. displacement vectors)
        
    Returns:
        Displaced mesh
        
    Raises:
        ValueError: If displacement_field shape doesn't match vertices
        
    Example:
        >>> mesh = trimesh.load('base.stl')
        >>> displacement = np.random.rand(len(mesh.vertices))
        >>> displaced = apply_displacement(mesh, displacement, amplitude=2.0)
    """
    mesh_copy = mesh.copy()
    
    if along_normal:
        # Displace along normals
        if displacement_field.shape[0] != len(mesh.vertices):
            raise ValueError(
                f"Displacement field length {displacement_field.shape[0]} "
                f"doesn't match vertex count {len(mesh.vertices)}"
            )
        
        displacement = mesh.vertex_normals * displacement_field[:, np.newaxis]
        mesh_copy.vertices += amplitude * displacement
    else:
        # Direct displacement vectors
        if displacement_field.shape != mesh.vertices.shape:
            raise ValueError(
                f"Displacement field shape {displacement_field.shape} "
                f"doesn't match vertices shape {mesh.vertices.shape}"
            )
        
        mesh_copy.vertices += amplitude * displacement_field
    
    return mesh_copy


def smooth_mesh(
    mesh: trimesh.Trimesh,
    iterations: int = 3,
    lambda_factor: float = 0.5
) -> trimesh.Trimesh:
    """Apply Laplacian smoothing to mesh.
    
    Args:
        mesh: Input mesh
        iterations: Number of smoothing iterations
        lambda_factor: Smoothing strength (0-1)
        
    Returns:
        Smoothed mesh
        
    Example:
        >>> mesh = trimesh.load('rough.stl')
        >>> smoothed = smooth_mesh(mesh, iterations=5, lambda_factor=0.3)
    """
    mesh_copy = mesh.copy()
    
    for _ in range(iterations):
        # Compute vertex neighbors
        vertex_neighbors = mesh_copy.vertex_neighbors
        
        # Laplacian smoothing
        new_vertices = mesh_copy.vertices.copy()
        for i, neighbors in enumerate(vertex_neighbors):
            if len(neighbors) > 0:
                neighbor_mean = mesh_copy.vertices[neighbors].mean(axis=0)
                new_vertices[i] = (
                    (1 - lambda_factor) * mesh_copy.vertices[i] +
                    lambda_factor * neighbor_mean
                )
        
        mesh_copy.vertices = new_vertices
    
    return mesh_copy


def validate_mesh(mesh: trimesh.Trimesh) -> Dict[str, Any]:
    """Validate mesh for 3D printing and general quality.
    
    This is the comprehensive validation function used by CLI tools
    and pipelines. Returns detailed validation results including
    statistics, warnings, and errors.
    
    Args:
        mesh: Mesh to validate
        
    Returns:
        Dictionary with validation results including:
        - is_valid: Overall validity boolean
        - is_watertight: Whether mesh is watertight
        - is_winding_consistent: Whether face winding is consistent
        - num_vertices: Number of vertices
        - num_faces: Number of faces
        - volume: Mesh volume (if solid)
        - surface_area: Surface area
        - bounds: Bounding box
        - dimensions: Physical dimensions (x, y, z)
        - warnings: List of warning messages
        - errors: List of error messages
        - degenerate_faces: Count of degenerate faces (if any)
        - duplicate_vertices: Count of duplicate vertices (if any)
        
    Example:
        >>> mesh = trimesh.load('model.stl')
        >>> results = validate_mesh(mesh)
        >>> if results['is_valid']:
        ...     print("Mesh is ready for printing!")
    """
    results: Dict[str, Any] = {
        'is_valid': True,
        'is_watertight': mesh.is_watertight,
        'is_winding_consistent': mesh.is_winding_consistent,
        'num_vertices': len(mesh.vertices),
        'num_faces': len(mesh.faces),
        'volume': mesh.volume if mesh.is_volume else None,
        'surface_area': mesh.area,
        'bounds': mesh.bounds,
        'warnings': [],
        'errors': []
    }
    
    # Check watertight
    if not mesh.is_watertight:
        results['is_valid'] = False
        results['errors'].append("Mesh is not watertight (has holes)")
    
    # Check winding
    if not mesh.is_winding_consistent:
        results['warnings'].append("Face winding is inconsistent")
    
    # Check for degenerate faces
    degenerate = np.isclose(mesh.area_faces, 0).sum()
    if degenerate > 0:
        results['is_valid'] = False
        results['errors'].append(f"Found {degenerate} degenerate faces (zero area)")
        results['degenerate_faces'] = int(degenerate)
    
    # Check for duplicate vertices
    unique_verts = len(np.unique(mesh.vertices, axis=0))
    duplicates = len(mesh.vertices) - unique_verts
    if duplicates > 0:
        results['warnings'].append(f"Found {duplicates} duplicate vertices")
        results['duplicate_vertices'] = int(duplicates)
    
    # Check for self-intersections (expensive, skip for large meshes)
    if len(mesh.faces) < 50000:
        if not mesh.is_volume:
            results['warnings'].append("Mesh may have self-intersections or is not a volume")
    
    # Compute bounding box dimensions
    bounds = mesh.bounds
    size = bounds[1] - bounds[0]
    results['dimensions'] = {
        'x': float(size[0]),
        'y': float(size[1]),
        'z': float(size[2])
    }
    
    # Add boolean flags for compatibility with pipelines that expect simpler interface
    results['has_degenerate_faces'] = degenerate > 0
    results['has_duplicate_vertices'] = duplicates > 0
    results['is_volume'] = mesh.is_volume
    
    return results


def decimate_mesh(
    mesh: trimesh.Trimesh,
    target_faces: int
) -> trimesh.Trimesh:
    """Reduce number of faces in mesh.
    
    Args:
        mesh: Input mesh
        target_faces: Target number of faces
        
    Returns:
        Decimated mesh
        
    Example:
        >>> mesh = trimesh.load('high_res.stl')
        >>> low_res = decimate_mesh(mesh, target_faces=10000)
    """
    if len(mesh.faces) <= target_faces:
        return mesh
    
    # Use trimesh simplification
    simplified = mesh.simplify_quadric_decimation(target_faces)
    
    return simplified


def repair_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Attempt to repair common mesh issues.
    
    Performs multiple repair operations:
    - Merges duplicate vertices
    - Removes degenerate faces
    - Removes duplicate faces
    - Fills holes (if possible)
    - Fixes normals
    
    Args:
        mesh: Input mesh
        
    Returns:
        Repaired mesh
        
    Example:
        >>> mesh = trimesh.load('broken.stl')
        >>> fixed = repair_mesh(mesh)
    """
    mesh_copy = mesh.copy()
    
    # Remove duplicate vertices
    mesh_copy.merge_vertices()
    
    # Remove degenerate faces
    mesh_copy.remove_degenerate_faces()
    
    # Remove duplicate faces
    mesh_copy.remove_duplicate_faces()
    
    # Fill holes (if applicable)
    if not mesh_copy.is_watertight:
        try:
            mesh_copy.fill_holes()
        except Exception:
            pass  # Hole filling can fail on complex geometry
    
    # Fix normals
    if not mesh_copy.is_winding_consistent:
        mesh_copy.fix_normals()
    
    return mesh_copy


def compute_overhang_analysis(
    mesh: trimesh.Trimesh,
    overhang_angle: float = 45.0
) -> Dict[str, Any]:
    """Analyse mesh for 3D printing overhangs.
    
    Determines which faces would require support material
    when printing in a given orientation.
    
    Args:
        mesh: Mesh to analyse
        overhang_angle: Angle in degrees beyond which support is needed
                       (measured from horizontal)
        
    Returns:
        Dictionary with analysis results:
        - overhang_percentage: Percentage of faces requiring support
        - num_overhang_faces: Number of faces requiring support
        - total_faces: Total number of faces
        - needs_supports: Boolean indicating if supports are recommended
        
    Example:
        >>> mesh = trimesh.load('model.stl')
        >>> analysis = compute_overhang_analysis(mesh, overhang_angle=45.0)
        >>> if analysis['needs_supports']:
        ...     print(f"{analysis['overhang_percentage']:.1f}% requires supports")
    """
    # Compute face normals
    normals = mesh.face_normals
    
    # Check how many faces point downward beyond threshold
    z_component = normals[:, 2]
    threshold = -np.cos(np.deg2rad(overhang_angle))
    
    downward_facing = z_component < threshold
    overhang_percentage = (downward_facing.sum() / len(normals)) * 100
    
    return {
        'overhang_percentage': float(overhang_percentage),
        'num_overhang_faces': int(downward_facing.sum()),
        'total_faces': len(normals),
        'needs_supports': overhang_percentage > 20.0
    }


def slice_mesh_horizontal(
    mesh: trimesh.Trimesh,
    z_height: float
) -> np.ndarray:
    """Slice mesh at a given height and return 2D contour.
    
    Useful for generating 2D profiles from 3D meshes.
    
    Args:
        mesh: Mesh to slice
        z_height: Z height at which to slice
        
    Returns:
        Array of 2D contour points (N, 2) in (x, y) coordinates
        
    Example:
        >>> mesh = trimesh.load('vase.stl')
        >>> contour = slice_mesh_horizontal(mesh, z_height=50.0)
        >>> plt.plot(contour[:, 0], contour[:, 1])
    """
    # Use trimesh's section method
    section = mesh.section(plane_origin=[0, 0, z_height],
                          plane_normal=[0, 0, 1])
    
    if section is None:
        return np.array([])
    
    # Get 2D coordinates
    coords, _ = section.to_planar()
    
    return coords.vertices


def create_field_from_pattern(
    pattern_2d: np.ndarray,
    height_samples: int,
    extrude_height: float = 1.0
) -> np.ndarray:
    """Create 3D field by extruding 2D pattern.
    
    Args:
        pattern_2d: 2D pattern array
        height_samples: Number of samples in height dimension
        extrude_height: Physical height of extrusion
        
    Returns:
        3D field array
        
    Example:
        >>> pattern = np.random.rand(100, 100)
        >>> field = create_field_from_pattern(pattern, height_samples=50)
    """
    h, w = pattern_2d.shape
    field_3d = np.zeros((h, w, height_samples), dtype=pattern_2d.dtype)
    
    # Simple extrusion
    for i in range(height_samples):
        field_3d[:, :, i] = pattern_2d
    
    return field_3d


def remesh_uniform(
    mesh: trimesh.Trimesh,
    target_edge_length: Optional[float] = None,
    target_faces: Optional[int] = None
) -> trimesh.Trimesh:
    """Remesh to uniform edge length or target face count.
    
    Args:
        mesh: Input mesh
        target_edge_length: Desired edge length (not yet implemented)
        target_faces: Desired number of faces
        
    Returns:
        Remeshed mesh
        
    Note:
        Uses trimesh's subdivision/decimation. For advanced remeshing,
        consider using PyMeshLab or other external tools.
        
    Example:
        >>> mesh = trimesh.load('irregular.stl')
        >>> uniform = remesh_uniform(mesh, target_faces=50000)
    """
    mesh_copy = mesh.copy()
    
    if target_faces:
        # Decimate or subdivide to reach target
        current_faces = len(mesh_copy.faces)
        
        if current_faces > target_faces:
            # Decimate
            mesh_copy = mesh_copy.simplify_quadric_decimation(target_faces)
        else:
            # Subdivide
            while len(mesh_copy.faces) < target_faces:
                mesh_copy = mesh_copy.subdivide()
                if len(mesh_copy.faces) > target_faces * 1.5:
                    # Overshoot, decimate back
                    mesh_copy = mesh_copy.simplify_quadric_decimation(target_faces)
                    break
    
    return mesh_copy
