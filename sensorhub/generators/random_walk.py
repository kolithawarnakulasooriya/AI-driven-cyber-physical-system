import numpy as np
from .base import SensorGenerator
from typing import Dict, Any

class RandomWalkGenerator(SensorGenerator):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        super().__init__(min_val, max_val, params)
        self.step_size = params.get("step_size", (max_val - min_val) / 20) if params else (max_val - min_val) / 20
        self.trend = params.get("trend", 0.0) if params else 0.0  # drift component
        self.current_value = (min_val + max_val) / 2

    def generate(self) -> float:
        random_step = np.random.normal(0, self.step_size)
        self.current_value += random_step + self.trend
        self.current_value = self.clamp(self.current_value)
        return self.current_value
