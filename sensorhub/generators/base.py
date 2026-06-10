from abc import ABC, abstractmethod
from typing import Dict, Any

class SensorGenerator(ABC):
    def __init__(self, min_val: float, max_val: float, params: Dict[str, Any] = None):
        self.min_val = min_val
        self.max_val = max_val
        self.params = params or {}

    @abstractmethod
    def generate(self) -> float:
        pass

    def clamp(self, value: float) -> float:
        return max(self.min_val, min(self.max_val, value))
