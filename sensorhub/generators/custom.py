import numpy as np
from .base import SensorGenerator
from typing import Dict, Any

class CustomGenerator(SensorGenerator):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        super().__init__(min_val, max_val, params)
        self.actual_value = (
            params.get("actual_value")
            if params and params.get("actual_value") is not None
            else (min_val + max_val) / 2
        )
        self.tolerance = (
            params.get("tolerance")
            if params and params.get("tolerance") is not None
            else 0.1 * (max_val - min_val)
        )
        if self.tolerance <= 0:
            self.tolerance = max(0.1, 0.01 * (max_val - min_val))

    def generate(self) -> float:
        value = np.random.normal(self.actual_value, self.tolerance)
        return self.clamp(value)
