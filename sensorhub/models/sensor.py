from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
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
    actual_value: float
    timestamp: datetime

    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "value": self.value,
            "actual_value": self.actual_value,
            "timestamp": self.timestamp.isoformat()
        }

class Sensor:
    def __init__(self, config: SensorConfig, sensor_id: str = None):
        self.id = sensor_id or str(uuid.uuid4())
        self.config = config
        self.is_running = False
        self.readings: list[SensorReading] = []
        self.recording = False
        self.current_value = (config.min_value + config.max_value) / 2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        config = SensorConfig(
            name=data["name"],
            sensor_type=data["type"],
            interval=data["interval"],
            min_value=data["min_value"],
            max_value=data["max_value"],
            parameters=data.get("parameters", {})
        )
        sensor = cls(config, sensor_id=data.get("id"))
        sensor.is_running = False
        sensor.recording = False
        sensor.current_value = data.get(
            "current_value",
            (config.min_value + config.max_value) / 2
        )
        return sensor

    def add_reading(self, value: float, actual_value: float = None):
        if actual_value is None:
            actual_value = value

        reading = SensorReading(
            sensor_id=self.id,
            value=value,
            actual_value=actual_value,
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
