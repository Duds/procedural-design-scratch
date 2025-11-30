"""Tests for mesh utility functions."""

import unittest
import numpy as np
import trimesh
from pathlib import Path
import tempfile

from src.utils.mesh import create_mesh, export_mesh


class TestMeshFunctions(unittest.TestCase):

    def test_create_mesh(self):
        """Test mesh creation with valid parameters."""
        # Create a simple triangular mesh
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 1.0, 0.0]
        ])
        faces = np.array([[0, 1, 2]])
        
        mesh = create_mesh(vertices, faces)
        
        self.assertIsInstance(mesh, trimesh.Trimesh)
        self.assertEqual(len(mesh.vertices), 3)
        self.assertEqual(len(mesh.faces), 1)

    def test_export_mesh(self):
        """Test exporting mesh to STL format."""
        # Create a simple mesh
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 1.0, 0.0]
        ])
        faces = np.array([[0, 1, 2]])
        mesh = create_mesh(vertices, faces)
        
        # Export to temporary file
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / 'test_mesh.stl'
            export_mesh(mesh, str(file_path), file_type='stl')
            self.assertTrue(file_path.exists())
            self.assertGreater(file_path.stat().st_size, 0)

    def test_export_mesh_unsupported_format(self):
        """Test that unsupported formats raise ValueError."""
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]])
        faces = np.array([[0, 1, 2]])
        mesh = create_mesh(vertices, faces)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / 'test_mesh.xyz'
            with self.assertRaises(ValueError):
                export_mesh(mesh, str(file_path), file_type='xyz')


if __name__ == '__main__':
    unittest.main()
