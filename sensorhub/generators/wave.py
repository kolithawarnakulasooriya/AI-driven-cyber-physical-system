import numpy as np
from .base import SensorGenerator
from typing import Dict, Any

class WaveGenerator(SensorGenerator):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        super().__init__(min_val, max_val, params)
        self.frequency = params.get("frequency", 0.1) if params else 0.1
        self.amplitude = params.get("amplitude", (max_val - min_val) / 2) if params else (max_val - min_val) / 2
        self.offset = params.get("offset", (min_val + max_val) / 2) if params else (min_val + max_val) / 2
        self.noise_level = params.get("noise_level", 0.02 * (max_val - min_val)) if params else 0.02 * (max_val - min_val)
        self.phase = 0

    def generate(self) -> float:
        wave_value = self.amplitude * np.sin(self.phase)
        noise = np.random.normal(0, self.noise_level)
        value = self.offset + wave_value + noise
        self.phase += self.frequency
        return self.clamp(value)
