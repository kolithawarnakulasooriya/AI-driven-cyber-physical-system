import csv
import os
from datetime import datetime
from typing import Optional

class CSVRecorder:
    def __init__(self, recordings_dir: str = "recordings"):
        self.recordings_dir = recordings_dir
        os.makedirs(recordings_dir, exist_ok=True)
        self.active_recorders: dict = {}

    def start_recording(self, sensor_id: str, sensor_name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{sensor_name}_{sensor_id}_{timestamp}.csv"
        filepath = os.path.join(self.recordings_dir, filename)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'value', 'actual_value'])

        self.active_recorders[sensor_id] = {
            'filepath': filepath,
            'filename': filename
        }
        return filename

    def write_reading(self, sensor_id: str, value: float, actual_value: float, timestamp: datetime):
        if sensor_id not in self.active_recorders:
            return

        filepath = self.active_recorders[sensor_id]['filepath']
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp.isoformat(), value, actual_value])

    def stop_recording(self, sensor_id: str) -> Optional[str]:
        if sensor_id in self.active_recorders:
            filename = self.active_recorders[sensor_id]['filename']
            del self.active_recorders[sensor_id]
            return filename
        return None

    def is_recording(self, sensor_id: str) -> bool:
        return sensor_id in self.active_recorders

    def get_active_recordings(self) -> dict:
        return {sid: info['filename'] for sid, info in self.active_recorders.items()}
