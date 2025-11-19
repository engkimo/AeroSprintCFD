import trimesh
import numpy as np

def create_demo_car(output_path="uploads/drivaer_demo.stl"):
    # Create a simplified car shape using primitives
    
    # 1. Main Body (Box)
    body = trimesh.creation.box(extents=[4.5, 1.8, 1.0])
    body.apply_translation([0, 0, 0.5]) # Lift up
    
    # 2. Cabin (Box, slightly smaller)
    cabin = trimesh.creation.box(extents=[2.5, 1.6, 0.8])
    cabin.apply_translation([-0.5, 0, 1.4])
    
    # 3. Wheels (Cylinders)
    wheels = []
    for x in [-1.5, 1.5]:
        for y in [-0.9, 0.9]:
            wheel = trimesh.creation.cylinder(radius=0.35, height=0.4)
            # Rotate to align with Y axis
            wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            wheel.apply_translation([x, y, 0.35])
            wheels.append(wheel)
            
    # Combine
    car = trimesh.util.concatenate([body, cabin] + wheels)
    
    # Smooth/Subdivide to look a bit more organic (optional, keeps it low poly for now)
    
    # Export
    car.export(output_path)
    print(f"Demo car saved to {output_path}")

if __name__ == "__main__":
    import os
    os.makedirs("uploads", exist_ok=True)
    create_demo_car()
