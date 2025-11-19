import trimesh
import numpy as np

def load_and_voxelize(file_path, resolution=64):
    """
    Loads an STL/OBJ and voxelizes it into a boolean grid.
    """
    mesh = trimesh.load(file_path)
    
    # Normalize mesh to fit in unit box (centered)
    mesh.apply_translation(-mesh.centroid)
    scale = 1.0 / np.max(mesh.extents)
    mesh.apply_scale(scale)
    
    # Voxelize
    # pitch = 1.0 / resolution
    voxel_grid = mesh.voxelized(pitch=1.0/resolution).fill()
    
    # Return the boolean matrix
    return voxel_grid.matrix, mesh
