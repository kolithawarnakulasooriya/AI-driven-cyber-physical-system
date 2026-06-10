import paho.mqtt.client as mqtt
from typing import Callable, Optional
import json

class MQTTHandler:
    def __init__(self):
        self.client = None
        self.connected = False
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        self.topic_prefix = "sensors"

    def set_callbacks(self, on_connect=None, on_disconnect=None):
        self.on_connect_callback = on_connect
        self.on_disconnect_callback = on_disconnect

    def connect(self, hostname: str, port: int = 1883, topic_prefix: str = "sensors") -> bool:
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.topic_prefix = topic_prefix

            self.client.connect(hostname, port, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"MQTT connection failed: {e}")
            return False

    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

    def publish(self, sensor_id: str, sensor_type: str, value: float, timestamp: str):
        if not self.connected or not self.client:
            return

        topic = f"{self.topic_prefix}/{sensor_id}/{sensor_type}"
        payload = json.dumps({
            "value": value,
            "timestamp": timestamp
        })
        self.client.publish(topic, payload)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            if self.on_connect_callback:
                self.on_connect_callback()
        else:
            print(f"MQTT connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        if self.on_disconnect_callback:
            self.on_disconnect_callback()

    def is_connected(self) -> bool:
        return self.connected
