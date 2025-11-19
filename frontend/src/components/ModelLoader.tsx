import { useStore } from '../store'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js'
import { useEffect, useState } from 'react'
import * as THREE from 'three'

export function ModelLoader() {
    const fileUrl = useStore((state) => state.fileUrl)
    const [geometry, setGeometry] = useState<THREE.BufferGeometry | null>(null)

    useEffect(() => {
        if (fileUrl) {
            const loader = new STLLoader()
            loader.load(fileUrl, (geo) => {
                geo.center()
                setGeometry(geo)
            })
        }
    }, [fileUrl])

    if (!geometry) return null

    return (
        <mesh geometry={geometry} castShadow receiveShadow>
            <meshStandardMaterial color="#ffffff" roughness={0.5} metalness={0.5} />
        </mesh>
    )
}
