import { useStore } from '../store'
import axios from 'axios'
import { Upload, Play, Settings } from 'lucide-react'

export function Controls() {
    const {
        file, setFile,
        resolution, setResolution,
        windSpeed, setWindSpeed,
        isSimulating, setSimulating,
        setSimulationResults
    } = useStore()

    const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0])
        }
    }

    const runSimulation = async () => {
        if (!file) return
        setSimulating(true)

        try {
            // 1. Upload file
            const formData = new FormData()
            formData.append('file', file)
            await axios.post('http://localhost:8000/upload', formData)

            // 2. Trigger simulation
            const res = await axios.post('http://localhost:8000/simulate', null, {
                params: { resolution, wind_speed: windSpeed }
            })

            setSimulationResults(res.data)
            setSimulating(false)

        } catch (error) {
            console.error(error)
            setSimulating(false)
        }
    }

    return (
        <div className="absolute top-4 left-4 bg-gray-800/80 backdrop-blur-md p-4 rounded-xl border border-gray-700 text-white w-80">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Settings className="w-5 h-5" /> Controls
            </h2>

            <div className="space-y-4">
                <div>
                    <label className="block text-sm text-gray-400 mb-1">Geometry (STL)</label>
                    <div className="relative">
                        <input
                            type="file"
                            accept=".stl"
                            onChange={handleUpload}
                            className="hidden"
                            id="file-upload"
                        />
                        <label
                            htmlFor="file-upload"
                            className="flex items-center justify-center gap-2 w-full py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded-lg cursor-pointer transition-colors"
                        >
                            <Upload className="w-4 h-4" />
                            {file ? file.name : "Upload STL"}
                        </label>
                    </div>
                </div>

                <div>
                    <label className="block text-sm text-gray-400 mb-1">Resolution: {resolution}</label>
                    <input
                        type="range"
                        min="32"
                        max="128"
                        step="32"
                        value={resolution}
                        onChange={(e) => setResolution(Number(e.target.value))}
                        className="w-full accent-blue-500"
                    />
                </div>

                <div>
                    <label className="block text-sm text-gray-400 mb-1">Wind Speed: {windSpeed} m/s</label>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={windSpeed}
                        onChange={(e) => setWindSpeed(Number(e.target.value))}
                        className="w-full accent-blue-500"
                    />
                </div>

                <button
                    onClick={runSimulation}
                    disabled={!file || isSimulating}
                    className={`w-full py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-all ${!file || isSimulating
                        ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20'
                        }`}
                >
                    {isSimulating ? (
                        <span className="animate-pulse">Simulating...</span>
                    ) : (
                        <>
                            <Play className="w-4 h-4" /> Start Simulation
                        </>
                    )}
                </button>
            </div>
        </div>
    )
}
