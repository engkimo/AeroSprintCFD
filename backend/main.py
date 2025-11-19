from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
from typing import List

app = FastAPI(title="AeroSprintCFD Backend")

# CORS Setup
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "AeroSprintCFD Backend is running"}

@app.post("/upload")
async def upload_geometry(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "path": file_path, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate")
async def simulate(
    file_path: str = "uploads/dummy.stl", 
    resolution: int = 64, 
    wind_speed: float = 10.0
):
    # 1. Load and Voxelize
    # For demo, we might need to find the latest uploaded file if not provided
    # Here we assume file_path is passed or we pick the only one in uploads
    
    files = os.listdir(UPLOAD_DIR)
    if not files:
        return {"error": "No file uploaded"}
    
    target_file = os.path.join(UPLOAD_DIR, files[-1]) # Pick latest
    
    from geometry import load_and_voxelize
    from solver import SimplePotentialFlowSolver
    import numpy as np
    
    voxel_matrix, mesh = load_and_voxelize(target_file, resolution=resolution)
    
    # 2. Solve
    solver = SimplePotentialFlowSolver(resolution=voxel_matrix.shape)
    solver.set_obstacles_from_voxel(voxel_matrix)
    v_x, v_y, v_z = solver.solve(iterations=200, inflow_velocity=wind_speed)
    
    # 3. Generate Streamlines (simplified for JSON response)
    # We will return a subset of velocity field or pre-computed streamlines
    # For "Millions of cells", sending the whole field is too big.
    # Let's generate some streamlines here.
    
    # Seed points: Plane at x=0
    seeds = []
    ny, nz = voxel_matrix.shape[1], voxel_matrix.shape[2]
    for y in range(0, ny, 4):
        for z in range(0, nz, 4):
            seeds.append([0, y, z])
            
    # Integrate streamlines
    streamlines = []
    dt = 0.5
    max_steps = 100
    
    for seed in seeds:
        path = [seed]
        curr = np.array(seed, dtype=float)
        for _ in range(max_steps):
            # Trilinear interpolation or nearest neighbor
            ix, iy, iz = int(curr[0]), int(curr[1]), int(curr[2])
            
            if ix < 0 or ix >= resolution or iy < 0 or iy >= ny or iz < 0 or iz >= nz:
                break
                
            vx = v_x[ix, iy, iz]
            vy = v_y[ix, iy, iz]
            vz = v_z[ix, iy, iz]
            
            # Simple Euler integration
            curr += np.array([vx, vy, vz]) * dt
            path.append(curr.tolist())
            
        streamlines.append(path)
        
    return {
        "status": "success",
        "resolution": resolution,
        "streamlines": streamlines
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
