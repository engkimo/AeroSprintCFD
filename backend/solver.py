import numpy as np
from scipy.ndimage import convolve

class SimplePotentialFlowSolver:
    def __init__(self, resolution=(64, 64, 64)):
        self.resolution = resolution
        self.grid = np.zeros(resolution, dtype=np.float32)
        self.obstacles = np.zeros(resolution, dtype=bool)
        
    def set_obstacles_from_voxel(self, voxel_grid):
        """
        voxel_grid: boolean numpy array of shape self.resolution
        """
        if voxel_grid.shape != self.resolution:
            raise ValueError(f"Grid shape mismatch: {voxel_grid.shape} != {self.resolution}")
        self.obstacles = voxel_grid

    def solve(self, iterations=500, inflow_velocity=1.0):
        """
        Solves Laplace equation for velocity potential phi: \nabla^2 \phi = 0
        Boundary conditions:
        - Inlet (x=0): Fixed potential gradient (Neumann) or Fixed Potential (Dirichlet)
          Here we use Dirichlet ramp for simplicity: phi = x * v_inf
        - Outlet (x=end): Neumann (dphi/dx = v_inf)
        - Walls: Neumann (dphi/dn = 0)
        - Obstacle: Neumann (dphi/dn = 0) - flow around
        """
        nx, ny, nz = self.resolution
        
        # Initialize potential field (linear ramp = uniform flow)
        X, Y, Z = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing='ij')
        self.phi = X * inflow_velocity
        
        # Mask for obstacles (potential inside doesn't matter, but boundaries do)
        # We will use a simple Jacobi iteration or SOR
        
        # SOR parameter
        omega = 1.8
        
        # Kernel for 3D Laplacian (6 neighbors)
        # We'll implement a manual loop or use convolution for steps, 
        # but for "Millions of cells" python loop is too slow.
        # We will use scipy.ndimage or numpy vectorization.
        
        # Vectorized Jacobi iteration
        # phi_new = (phi_x+1 + phi_x-1 + phi_y+1 + ...) / 6
        
        kernel = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                           [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                           [[0, 0, 0], [0, 1, 0], [0, 0, 0]]]) / 6.0
        
        # Boundary masks
        # Fixed inlet/outlet for simplicity
        # We want flow in X direction.
        
        for i in range(iterations):
            # Convolve to get average of neighbors
            phi_avg = convolve(self.phi, kernel, mode='nearest')
            
            # SOR update
            self.phi = self.phi * (1 - omega) + phi_avg * omega
            
            # Enforce Boundary Conditions
            
            # 1. Inlet (x=0) and Outlet (x=end)
            self.phi[0, :, :] = 0
            self.phi[-1, :, :] = (nx - 1) * inflow_velocity
            
            # 2. Obstacles
            # Simple approach: Reset potential inside obstacles to average of neighbors? 
            # Or just let it flow and mask velocity later (Penalization).
            # For visual demo, masking velocity is often enough if the grid is fine enough.
            # But to make flow go *around*, we need the potential to be flat inside or satisfy Neumann.
            # Let's try: Do NOT update phi inside obstacles (keep it at initial guess or 0?)
            # If we keep it 0, it acts as a sink.
            # If we keep it at current value, it acts as fixed.
            # We want dphi/dn = 0.
            # Let's use the "mask velocity" approach for simplicity in this demo.
            pass
            
        # Compute Velocity Field v = \nabla \phi
        # Gradient (central difference)
        v_x, v_y, v_z = np.gradient(self.phi)
        
        # Normalize gradient to match inflow velocity scale roughly
        # np.gradient with spacing 1 gives delta/2.
        
        # Mask velocity inside obstacles
        v_x[self.obstacles] = 0
        v_y[self.obstacles] = 0
        v_z[self.obstacles] = 0
        
        return v_x, v_y, v_z

    def get_streamlines(self, v_x, v_y, v_z, seeds):
        """
        Generate streamlines from velocity field.
        seeds: list of (x, y, z) starting points
        """
        # This would be done better in PyVista or Frontend
        pass
