import { useStore } from '../store'
import { useMemo } from 'react'
import * as THREE from 'three'
import { Line } from '@react-three/drei'

export function FlowVisualizer() {
    const results = useStore((state) => state.simulationResults)

    // Placeholder for streamlines
    // In a real implementation, we would parse 'results' (velocity field) and generate lines.
    // For now, we can show a dummy visualization if simulating.

    const lines = useMemo(() => {
        if (!results || !results.streamlines) return null

        // Parse streamlines from backend [[x,y,z], ...]
        // Backend returns list of paths, each path is list of points [x,y,z]
        // We need to scale them back to world space if needed, but here we assume 1:1 for now
        // or we might need to center them.
        // The backend voxel grid is 0..resolution. The mesh was normalized to 0..1?
        // Wait, geometry.py normalized mesh to unit box. Voxel grid is resolution size.
        // So we need to scale points by 1/resolution to match the mesh view?
        // Let's check geometry.py:
        // mesh.apply_scale(scale) -> fits in unit box.
        // voxel_grid = mesh.voxelized(pitch=1.0/resolution)
        // So the voxel indices 0..resolution map to 0..1 in world space.
        // So we divide by resolution.

        const resolution = results.resolution || 64

        return results.streamlines.map((path: number[][]) =>
            path.map(p => new THREE.Vector3(
                p[0] / resolution - 0.5, // Center it? Mesh was centered.
                p[1] / resolution - 0.5,
                p[2] / resolution - 0.5
            ))
        )
    }, [results])

    if (!results) return null

    return (
        <group>
            {lines?.map((linePoints: THREE.Vector3[], i: number) => (
                <Line
                    key={i}
                    points={linePoints}
                    color="cyan"
                    lineWidth={1}
                    opacity={0.5}
                    transparent
                />
            ))}
        </group>
    )
}

