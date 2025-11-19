import { create } from 'zustand'

interface SimulationState {
    file: File | null
    fileUrl: string | null
    resolution: number
    windSpeed: number
    isSimulating: boolean
    simulationResults: any | null
    setFile: (file: File) => void
    setResolution: (res: number) => void
    setWindSpeed: (speed: number) => void
    setSimulating: (isSimulating: boolean) => void
    setSimulationResults: (results: any) => void
}

export const useStore = create<SimulationState>((set) => ({
    file: null,
    fileUrl: null,
    resolution: 64,
    windSpeed: 10.0,
    isSimulating: false,
    simulationResults: null,
    setFile: (file) => set({ file, fileUrl: URL.createObjectURL(file) }),
    setResolution: (resolution) => set({ resolution }),
    setWindSpeed: (windSpeed) => set({ windSpeed }),
    setSimulating: (isSimulating) => set({ isSimulating }),
    setSimulationResults: (simulationResults) => set({ simulationResults }),
}))
