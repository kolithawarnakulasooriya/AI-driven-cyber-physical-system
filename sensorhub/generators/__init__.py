from .base import SensorGenerator
from .gaussian import GaussianGenerator
from .wave import WaveGenerator
from .random_walk import RandomWalkGenerator
from .custom import CustomGenerator

__all__ = [
    "SensorGenerator",
    "GaussianGenerator",
    "WaveGenerator",
    "RandomWalkGenerator",
    "CustomGenerator"
]

GENERATOR_MAP = {
    "gaussian": GaussianGenerator,
    "wave": WaveGenerator,
    "random_walk": RandomWalkGenerator,
    "lidar": RandomWalkGenerator,
    "custom": CustomGenerator
}

def get_generator(sensor_type: str, min_val: float, max_val: float, params=None):
    generator_class = GENERATOR_MAP.get(sensor_type)
    if not generator_class:
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    return generator_class(min_val, max_val, params)
