import { Viewer3D } from './components/Viewer3D'
import { Controls } from './components/Controls'

function App() {
    return (
        <div className="w-full h-screen bg-gray-900 text-white relative overflow-hidden">
            <Viewer3D />
            <Controls />

            <div className="absolute bottom-4 right-4 text-xs text-gray-500 pointer-events-none">
                AeroSprintCFD v0.1.0
            </div>
        </div>
    )
}

export default App
