from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

@dataclass
class SensorConfig:
    name: str
    sensor_type: str  # gaussian, wave, random_walk, lidar, custom
    interval: float  # seconds between readings
    min_value: float
    max_value: float
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SensorReading:
    sensor_id: str
    value: float
    timestamp: datetime

    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }

class Sensor:
    def __init__(self, config: SensorConfig):
        self.id = str(uuid.uuid4())
        self.config = config
        self.is_running = False
        self.readings: list[SensorReading] = []
        self.recording = False
        self.current_value = (config.min_value + config.max_value) / 2

    def add_reading(self, value: float):
        reading = SensorReading(
            sensor_id=self.id,
            value=value,
            timestamp=datetime.now()
        )
        self.readings.append(reading)
        self.current_value = value
        if len(self.readings) > 1000:
            self.readings = self.readings[-1000:]
        return reading

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.config.name,
            "type": self.config.sensor_type,
            "interval": self.config.interval,
            "min_value": self.config.min_value,
            "max_value": self.config.max_value,
            "is_running": self.is_running,
            "current_value": self.current_value,
            "recording": self.recording,
            "parameters": self.config.parameters
        }
