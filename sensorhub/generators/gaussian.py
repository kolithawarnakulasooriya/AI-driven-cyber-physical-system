import numpy as np
from .base import SensorGenerator
from typing import Dict, Any

class GaussianGenerator(SensorGenerator):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        super().__init__(min_val, max_val, params)
        self.mean = params.get("mean", (min_val + max_val) / 2) if params else (min_val + max_val) / 2
        self.std_dev = params.get("std_dev", (max_val - min_val) / 6) if params else (max_val - min_val) / 6
        self.drift = params.get("drift", 0.0) if params else 0.0
        self.current_mean = self.mean

    def generate(self) -> float:
        self.current_mean += self.drift
        value = np.random.normal(self.current_mean, self.std_dev)
        return self.clamp(value)
