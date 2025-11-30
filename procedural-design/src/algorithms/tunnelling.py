"""Agent-based tunnelling algorithms for 3D fields.

This module provides functions to carve tunnels or modify 3D scalar
fields using agent-based approaches such as random walks.
"""

from typing import Optional
import numpy as np


def carve_tunnels_random_walk(
    field: np.ndarray,
    mask: np.ndarray,
    n_agents: int = 10,
    agent_steps: int = 100,
    radius: float = 1.0,
    reduction_factor: float = 0.3,
    random_seed: Optional[int] = None
) -> np.ndarray:
    """Carve tunnels through a 3D scalar field using random walk agents.
    
    Agents perform random walks through the field, reducing field values
    in a spherical region around their position. Useful for creating
    perforations or tunnels in reaction-diffusion patterns.
    
    Args:
        field: 3D scalar field to modify
        mask: Boolean mask defining valid region (agents stay within mask)
        n_agents: Number of tunnelling agents
        agent_steps: Number of steps each agent takes
        radius: Tunnel radius (in grid units)
        reduction_factor: Multiplier for field values in tunnel region (0-1)
                          Lower values create deeper tunnels
        random_seed: Random seed for reproducibility
    
    Returns:
        Modified field with tunnels carved
        
    Example:
        >>> field = np.random.rand(64, 64, 64)
        >>> mask = np.ones((64, 64, 64), dtype=bool)
        >>> tunnelled = carve_tunnels_random_walk(
        ...     field, mask, n_agents=5, agent_steps=50, radius=2.0
        ... )
    """
    if n_agents <= 0 or agent_steps <= 0:
        return field.copy()
    
    n = field.shape[0]
    rng = np.random.default_rng(random_seed)
    coords = np.array(np.where(mask)).T
    
    if len(coords) == 0:
        return field.copy()
    
    f = field.copy()
    
    for _ in range(n_agents):
        # Start agent at random position within mask
        x, y, z = coords[rng.integers(0, len(coords))]
        
        for _ in range(agent_steps):
            # Define carving region
            xs = slice(max(0, int(x - radius)), min(n, int(x + radius + 1)))
            ys = slice(max(0, int(y - radius)), min(n, int(y + radius + 1)))
            zs = slice(max(0, int(z - radius)), min(n, int(z + radius + 1)))
            
            # Create distance mask for spherical carving
            X, Y, Z = np.meshgrid(
                np.arange(xs.start, xs.stop),
                np.arange(ys.start, ys.stop),
                np.arange(zs.start, zs.stop),
                indexing="ij",
            )
            R = np.sqrt((X - x)**2 + (Y - y)**2 + (Z - z)**2)
            carve_mask = R <= radius
            
            # Reduce field values in tunnel region
            f[xs, ys, zs][carve_mask] *= reduction_factor
            
            # Random walk step
            dx, dy, dz = rng.integers(-1, 2, size=3)
            x = np.clip(x + dx, 0, n - 1)
            y = np.clip(y + dy, 0, n - 1)
            z = np.clip(z + dz, 0, n - 1)
            
            # If agent leaves mask, restart at random position
            if not mask[int(x), int(y), int(z)]:
                x, y, z = coords[rng.integers(0, len(coords))]
    
    return f

