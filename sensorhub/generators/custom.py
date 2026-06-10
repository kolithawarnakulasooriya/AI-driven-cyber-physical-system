import numpy as np
from .base import SensorGenerator
from typing import Dict, Any

class CustomGenerator(SensorGenerator):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        super().__init__(min_val, max_val, params)
        self.pattern = params.get("pattern", "linear") if params else "linear"  # linear, exponential, random
        self.step = 0
        self.total_steps = params.get("total_steps", 100) if params else 100
        self.noise_level = params.get("noise_level", 0.01 * (max_val - min_val)) if params else 0.01 * (max_val - min_val)

    def generate(self) -> float:
        range_val = self.max_val - self.min_val

        if self.pattern == "linear":
            progress = (self.step % self.total_steps) / self.total_steps
            value = self.min_val + progress * range_val
        elif self.pattern == "exponential":
            progress = (self.step % self.total_steps) / self.total_steps
            value = self.min_val + (np.exp(progress) - 1) / (np.e - 1) * range_val
        else:  # random
            value = np.random.uniform(self.min_val, self.max_val)

        noise = np.random.normal(0, self.noise_level)
        self.step += 1
        return self.clamp(value + noise)
