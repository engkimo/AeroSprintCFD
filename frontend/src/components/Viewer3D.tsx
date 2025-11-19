import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stage, Environment, Grid } from '@react-three/drei'
import { Suspense } from 'react'
import { ModelLoader } from './ModelLoader'
import { FlowVisualizer } from './FlowVisualizer'

export function Viewer3D() {
    return (
        <div className="w-full h-full bg-gray-900">
            <Canvas shadows camera={{ position: [4, 4, 4], fov: 50 }}>
                <Suspense fallback={null}>
                    <Stage environment="city" intensity={0.5}>
                        <ModelLoader />
                        <FlowVisualizer />
                    </Stage>
                    <Grid infiniteGrid fadeDistance={50} fadeStrength={5} />
                </Suspense>
                <OrbitControls makeDefault />
                <Environment preset="city" />
            </Canvas>
        </div>
    )
}
